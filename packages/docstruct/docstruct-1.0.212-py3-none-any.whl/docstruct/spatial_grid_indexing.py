from .point import Point
from .visual_detection.vis_line import VisLine
from .bounding_box import BoundingBox
import numpy as np


class SpatialGrid:
    def __init__(self, num_rows: int, num_cols: int):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.grid = np.empty((num_rows, num_cols), dtype=object)

    def convert_to_grid_coordinates(self, point: Point) -> tuple[int, int]:
        """Convert a point to grid coordinates."""
        return (
            int(point.x * self.num_cols),
            int(point.y * self.num_rows),
        )

    def add_to_grid(self, grid_x: int, grid_y: int, data: object):
        if self.grid[grid_y, grid_x] is None:
            self.grid[grid_y, grid_x] = set([data])
        else:
            self.grid[grid_y, grid_x].add(data)

    def get_from_grid(self, point: Point) -> set:
        grid_x, grid_y = self.convert_to_grid_coordinates(point)
        return self.grid[grid_y, grid_x]

    def add_point(self, point: Point, data: object = None):
        data = data or point
        grid_x, grid_y = self.convert_to_grid_coordinates(point)
        self.add_to_grid(grid_x, grid_y, data)

    def add_bounding_box_center(self, bbox: BoundingBox, data: object = None):
        data = data or bbox
        self.add_point(bbox.get_center(), data)

    def add_bounding_box_corners(self, bbox: BoundingBox, data: object = None):
        data = data or bbox
        self.add_point(bbox.get_top_left(), data)
        self.add_point(bbox.get_top_right(), data)
        self.add_point(bbox.get_bottom_left(), data)
        self.add_point(bbox.get_bottom_right(), data)

    def add_bounding_box_exterior(self, bbox: BoundingBox, data: object = None):
        data = data or bbox
        start_x, start_y = self.convert_to_grid_coordinates(bbox.get_bottom_left())
        end_x, end_y = self.convert_to_grid_coordinates(bbox.get_top_right())
        for x in range(start_x, end_x + 1):
            self.add_to_grid(x, start_y, data)
            self.add_to_grid(x, end_y, data)
        for y in range(start_y, end_y + 1):
            self.add_to_grid(start_x, y, data)
            self.add_to_grid(end_x, y, data)

    def add_bounding_box_interior(
        self,
        bbox: BoundingBox,
        data: object = None,
    ):
        data = data or bbox
        start_x, start_y = self.convert_to_grid_coordinates(bbox.get_bottom_left())
        end_x, end_y = self.convert_to_grid_coordinates(bbox.get_top_right())

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                self.add_to_grid(x, y, data)

    def add_vis_line(self, vis_line: VisLine, data: object = None):
        data = data or vis_line
        if vis_line.orientation == VisLine.Orientation.HORIZONTAL:
            start_x, start_y = self.convert_to_grid_coordinates(
                Point(vis_line.start, vis_line.axis)
            )
            end_x, end_y = self.convert_to_grid_coordinates(
                Point(vis_line.end, vis_line.axis)
            )
            for x in range(start_x, end_x + 1):
                self.add_to_grid(x, start_y, data)
        elif vis_line.orientation == VisLine.Orientation.VERTICAL:
            start_x, start_y = self.convert_to_grid_coordinates(
                Point(vis_line.axis, vis_line.start)
            )
            end_x, end_y = self.convert_to_grid_coordinates(
                Point(vis_line.axis, vis_line.end)
            )
            for y in range(start_y, end_y + 1):
                self.add_to_grid(start_x, y, data)
