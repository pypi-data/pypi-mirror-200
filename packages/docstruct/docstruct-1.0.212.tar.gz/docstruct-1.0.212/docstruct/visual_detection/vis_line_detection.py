from ast import Or
import numpy as np
import cv2
import numpy as np
import math
from .vis_line import VisLine, Orientation
from ..bounding_box import BoundingBox
from ..graph import Node, Graph
from .constants import (
    AXIS_DELTA_NET_PARTITION,
    ANGLE_DEGREE_THRESHOLD,
    WIDTH_SCALE,
    HEIGHT_SCALE,
    NUM_SAMPLED_POINTS_ON_LINE,
    NUM_SAMPLED_POINTS_ON_ORTHOGONAL_LINE,
)


class VisLineDetector:
    def __init__(self, image: np.ndarray[(int, int)], length_threshold: float):
        self.image = image
        self.length_threshold = length_threshold
        self.image_height, self.image_width = image.shape
        self.id_generator = self.get_id_generator()

    @staticmethod
    def is_hor_line(line: np.array) -> bool:
        line_angle = VisLineDetector.get_line_angle(line)
        return VisLineDetector.is_hor_angle(line_angle)

    @staticmethod
    def is_ver_line(line: np.array) -> bool:
        line_angle = VisLineDetector.get_line_angle(line)
        return VisLineDetector.is_ver_angle(line_angle)

    @staticmethod
    def is_hor_angle(angle: float) -> bool:
        return -ANGLE_DEGREE_THRESHOLD < angle < ANGLE_DEGREE_THRESHOLD

    @staticmethod
    def is_ver_angle(angle: float) -> bool:
        return 90 - ANGLE_DEGREE_THRESHOLD < angle < 90 + ANGLE_DEGREE_THRESHOLD

    @staticmethod
    def get_line_angle(line: np.array) -> float:
        x0, y0, x1, y1 = line
        delta_x = abs(x0 - x1)
        delta_y = abs(y0 - y1)
        line_angle = math.degrees(math.atan2(delta_y, delta_x))
        return line_angle

    @staticmethod
    def fix_orientation(line: np.ndarray):
        x0, y0, x1, y1 = line
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        return x0, y0, x1, y1

    def get_openCV_lines(self):
        line_detector = cv2.ximgproc.createFastLineDetector(
            canny_th1=50,
            canny_th2=50,
            length_threshold=self.length_threshold,
            do_merge=True,
        )
        lines = line_detector.detect(self.image)
        if lines is None:
            return None
        return lines.squeeze(1)

    def normalize_line_coordinates(self, line: np.array):
        x0, y0, x1, y1 = line
        x0 = x0 / self.image_width
        x1 = x1 / self.image_width
        y0 = 1 - y0 / self.image_height
        y1 = 1 - y1 / self.image_height
        return x0, y0, x1, y1

    def get_line_width(self, line: dict, orientation: Orientation):
        x0, y0, x1, y1 = line
        points = sample_points_on_line(x0, y0, x1, y1, NUM_SAMPLED_POINTS_ON_LINE)
        widths = []
        for point in points:
            # TODO think of a max_length
            max_length = 15
            orthogonal_line = get_line(
                *point,
                length=max_length,
                orientation=Orientation.get_orthogonal(orientation),
            )

            orthogonal_points = sample_points_on_line(
                *orthogonal_line, NUM_SAMPLED_POINTS_ON_ORTHOGONAL_LINE
            )
            orthogonal_pixels_value = [
                get_pixel_value_with_interpolation(self.image, *point)
                for point in orthogonal_points
            ]
            width = estimate_width_from_pixels(orthogonal_pixels_value)
            widths.append(width)
        return np.mean(widths)

    def get_id_generator(self):
        i = 0
        while True:
            yield i
            i += 1

    def convert_to_vis_line(
        self, openCV_line: np.array, orientation: Orientation
    ) -> VisLine:
        line_width = self.get_line_width(openCV_line, orientation)
        normalized_line = self.normalize_line_coordinates(line=openCV_line)
        normalized_oriented_line = VisLineDetector.fix_orientation(normalized_line)
        normalized_line_width = line_width / self.image_height
        if orientation == Orientation.HORIZONTAL:
            axis = (normalized_oriented_line[1] + normalized_oriented_line[3]) / 2
            start = normalized_oriented_line[0]
            end = normalized_oriented_line[2]
        else:
            axis = (normalized_oriented_line[0] + normalized_oriented_line[2]) / 2
            start = normalized_oriented_line[1]
            end = normalized_oriented_line[3]
        return VisLine(
            axis=axis,
            orientation=orientation,
            start=start,
            end=end,
            width=normalized_line_width,
            id=next(self.id_generator),
        )

    def main(self):
        openCV_lines = self.get_openCV_lines()
        if openCV_lines is None:
            return [], []
        openCV_hor_lines = [
            line for line in openCV_lines if VisLineDetector.is_hor_line(line)
        ]
        openCV_ver_lines = [
            line for line in openCV_lines if VisLineDetector.is_ver_line(line)
        ]
        vis_hor_lines = [
            self.convert_to_vis_line(line, orientation=Orientation.HORIZONTAL)
            for line in openCV_hor_lines
        ]
        vis_ver_lines = [
            self.convert_to_vis_line(line, orientation=Orientation.VERTICAL)
            for line in openCV_ver_lines
        ]
        return vis_hor_lines, vis_ver_lines


class VisLineMerger:
    def __init__(self, lines: list[VisLine], length_threshold: float):
        self.lines = lines
        self.length_threshold = length_threshold

    def get_axis_delta_net(self, partition_factor):
        axis_delta_net = {}
        for line in self.lines:
            axis_value = line.axis
            index = int(axis_value * partition_factor)
            if index not in axis_delta_net:
                axis_delta_net[index] = [line]
            else:
                axis_delta_net[index].append(line)
        return axis_delta_net

    def get_graph(
        self,
        axis_delta_net: dict,
        delta_net_partition_factor: int,
    ):
        """
        In order for two lines to be adjacent, they must be at most at a distance of ver_epsilon from each other on the y axis
        Given two lines with axis_value x and y and assume |x-y| <= ver_epsilon
        --> x <= y + ver_epsilon -->
        int(x * partition_factor) <= int((y + ver_epsilon)*partition_factor) <= int(y*partition_factor) + int(ver_epsilon*partition_factor) + 1
        --> x_index <= y_index + int(ver_epsilon*partition_factor) + 1
        From symmetry we have |x_index - y_index| <= int(ver_epsilon*partition_factor) + 1
        """
        nodes = [Node(line) for line in self.lines]

        map_line_id_to_node = {
            line.id: nodes[index] for index, line in enumerate(self.lines)
        }

        max_index_shift = int(WIDTH_SCALE * delta_net_partition_factor) + 1
        for first_line in self.lines:
            axis_value = first_line.axis
            first_delta_net_index = int(axis_value * delta_net_partition_factor)
            for second_delta_net_index in range(
                first_delta_net_index - max_index_shift,
                first_delta_net_index + max_index_shift + 1,
            ):
                close_lines = axis_delta_net.get(second_delta_net_index, [])
                for second_line in close_lines:
                    if first_line.id == second_line.id:
                        continue

                    if self.are_adjacent_lines(first_line, second_line):
                        map_line_id_to_node[first_line.id].add_neighbor(
                            map_line_id_to_node[second_line.id]
                        )
        return Graph(nodes)

    def get_weighted_average_axis(self, lines: list["VisLine"]) -> float:
        """Get the weighted average of the axis values of a list of visual lines."""
        return np.average(
            [line.axis for line in lines],
            weights=[(vis_line.get_length()) for vis_line in lines],
        )

    def merge_connected_component(self, lines: list[VisLine]):
        """
        Merge a connected component of horizontal lines
        """
        if len(lines) == 1:
            return lines[0]

        start_values = [line.start for line in lines]
        end_values = [line.end for line in lines]
        width_values = [line.width for line in lines]
        return VisLine(
            axis=self.get_weighted_average_axis(lines),
            orientation=lines[0].orientation,
            start=np.min(start_values),
            end=np.max(end_values),
            width=np.mean(width_values),
            id=lines[0].id,
        )

    def main(self):
        """
        Merge horizontal lines that are close to each other
        A line with axis_value = axis and a width = W, is represented by a bounding box surrounding that line
        with width = W(1+hor_epsilon) and hight = ver_epsilon
        two lines are adjacent of their bounding boxes intersect.
        First notice int(x+y) <= int(x)+int(y)+1
        """
        axis_delta_net = self.get_axis_delta_net(
            partition_factor=AXIS_DELTA_NET_PARTITION
        )
        graph = self.get_graph(
            axis_delta_net,
            AXIS_DELTA_NET_PARTITION,
        )
        ccs_of_nodes = graph.get_connected_components()

        ccs_of_lines = []
        for cc in ccs_of_nodes:
            ccs_of_lines.append([node.data for node in cc])

        merged_lines = []
        for cc in ccs_of_lines:
            line = self.merge_connected_component(cc)
            merged_lines.append(line)
        return merged_lines

    def are_adjacent_lines(
        self,
        first_line: VisLine,
        second_line: VisLine,
    ):
        first_bb = first_line.convert_to_bb(
            height_scale=HEIGHT_SCALE,
            width_scale=WIDTH_SCALE,
            length_threshold=self.length_threshold,
        )
        second_bb = second_line.convert_to_bb(
            height_scale=HEIGHT_SCALE,
            width_scale=WIDTH_SCALE,
            length_threshold=self.length_threshold,
        )
        return first_bb.intersect(second_bb)


def sample_points_on_line(x0, y0, x1, y1, num_points: int) -> np.ndarray:
    """
    Sample equidistant points on a line segment avoiding the endpoints
    """
    x = np.linspace(x0, x1, num_points + 2)[1:-1]
    y = np.linspace(y0, y1, num_points + 2)[1:-1]
    return np.stack([x, y], axis=1)


def get_pixel_value(image: np.ndarray, x: int, y: int):
    try:
        return image[y, x]
    except IndexError:
        return 255


def get_pixel_value_with_interpolation(image: np.ndarray, x: float, y: float):
    """
    Notice the sum of the weights is equal to 1:
    """
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1
    x0_weight = x1 - x
    x1_weight = x - x0
    y0_weight = y1 - y
    y1_weight = y - y0
    return (
        get_pixel_value(image, x0, y0) * x0_weight * y0_weight
        + get_pixel_value(image, x1, y0) * x1_weight * y0_weight
        + get_pixel_value(image, x0, y1) * x0_weight * y1_weight
        + get_pixel_value(image, x1, y1) * x1_weight * y1_weight
    )


def estimate_width_from_pixels(pixels: list[int]):
    # TODO - for the "001" case in the dataset with boundaries width of 5 doesn't work good.
    return 10


def get_line(center_x: float, center_y: float, length: float, orientation: Orientation):
    if orientation == Orientation.HORIZONTAL:
        x0 = center_x - length / 2
        x1 = center_x + length / 2
        y0 = center_y
        y1 = center_y
    else:
        x0 = center_x
        x1 = center_x
        y0 = center_y - length / 2
        y1 = center_y + length / 2
    return x0, y0, x1, y1


def filter_lines_by_length(
    lines: list[VisLine], length_threshold: float
) -> list[VisLine]:
    return [line for line in lines if line.get_length() > length_threshold]
