from enum import Enum
import logging
from ..bounding_box import BoundingBox


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

    @staticmethod
    def get_orthogonal(orientation: "Orientation") -> "Orientation":
        if orientation == Orientation.HORIZONTAL:
            return Orientation.VERTICAL
        elif orientation == Orientation.VERTICAL:
            return Orientation.HORIZONTAL


class VisLine:
    def __init__(
        self,
        axis: float,
        orientation: Orientation,
        start: float,
        end: float,
        width: float,
        id: int,
    ):
        self.axis = axis
        self.orientation = orientation
        self.start = start
        self.end = end
        self.width = width
        self.id = id
        self.valid_args()

    def valid_args(self) -> bool:
        if self.start >= self.end:
            logging.error("Invalid VisLine: start >= end")

    def __str__(self):
        return f"VisLine(axis_value={self.axis}, orientation={self.orientation}, start={self.start}, end={self.end}, width={self.width}))"

    def __repr__(self):
        return self.__str__()

    def get_width(self) -> float:
        return self.width

    def get_length(self) -> float:
        return self.end - self.start

    def get_center(self) -> float:
        return (self.start + self.end) / 2

    def convert_to_bb(self, height_scale=1, width_scale=1, length_threshold=0):
        new_length = self.get_length() * (1 + height_scale) + length_threshold
        new_width = self.get_width() * (1 + width_scale)

        if self.orientation == Orientation.HORIZONTAL:
            left = self.get_center() - new_length / 2
            right = self.get_center() + new_length / 2
            top = self.axis + new_width / 2
            bottom = self.axis - new_width / 2
        else:
            left = self.axis - new_width / 2
            right = self.axis + new_width / 2
            top = self.get_center() + new_length / 2
            bottom = self.get_center() - new_length / 2
        return BoundingBox(left, top, right, bottom)
