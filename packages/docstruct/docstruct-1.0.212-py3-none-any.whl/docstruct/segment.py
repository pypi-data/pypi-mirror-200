class Segment:
    """
    A segment in 1D space.
    """

    def __init__(self, left: float, right: float):
        self.left = left
        self.right = right
        self.validate_args()

    def validate_args(self):
        """Check if the arguments are valid."""
        if self.left > self.right:
            raise ValueError(f"left={self.left} is greater than right={self.right}")

    def get_left(self) -> float:
        """Get the left value of the segment."""
        return self.left

    def get_right(self) -> float:
        """Get the right value of the segment."""
        return self.right

    def get_length(self) -> float:
        """Get the length of the segment."""
        return abs(self.right - self.left)

    def get_center(self) -> float:
        """Get the center of the segment."""
        return (self.left + self.right) / 2

    def __lt__(self, other):
        return self.right < other.left

    def __gt__(self, other):
        return self.left > other.right

    def __str__(self):
        return f"Segment(left={self.left:.3f}, right={self.right:.3f})"

    def __repr__(self):
        return self.__str__()

    def intersect(self, other: "Segment"):
        """Check if two segments intersect"""
        if self.left > other.right:
            return False
        if self.right < other.left:
            return False
        return True

    def merge(self, other: "Segment") -> "Segment":
        """Merge two segments assuming that they intersect."""
        return Segment(min(self.left, other.left), max(self.right, other.right))

    def relation(self, other: "Segment") -> int:
        """Check the relation between two segments.
        Returns -1 if the other segment is before the self segment.
        Returns 0 if there is intersection between self and other.
        Returns 1 if the self segment is before the other segment.

        """
        if self < other:
            return 1
        if other < self:
            return -1
        return 0

    @staticmethod
    def merge_segments(segments: list["Segment"]) -> list["Segment"]:
        """
        Merge every segments that intersect with each other to a single segment.
        The output is a list of segments that are not intersecting.
        Moreover the output is increasingly sorted.
        """
        if len(segments) <= 1:
            return segments
        segments = sorted(segments, key=lambda segment: segment.get_left())

        clusters: list[Segment] = [segments.pop(0)]
        for segment in segments:
            last_cluster = clusters[-1]
            if segment.intersect(last_cluster):
                clusters[-1] = last_cluster.merge(segment)

            else:
                clusters.append(segment)
        return clusters
