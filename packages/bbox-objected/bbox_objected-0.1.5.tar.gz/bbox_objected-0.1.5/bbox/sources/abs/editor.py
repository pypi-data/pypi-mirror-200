from abc import ABC

from ..bbox_getter import BBoxGetter


class AbsBBoxEditor(BBoxGetter, ABC):
    def round_coords(self) -> None:
        self.x1 = round(self.x1)
        self.y1 = round(self.y1)
        self.x2 = round(self.x2)
        self.y2 = round(self.y2)

    def move_basis(self, x: int, y: int) -> None:
        self.x1 += x
        self.x2 += x
        self.y1 += y
        self.y2 += y

    def zero_basis(self) -> None:
        self.x2 = self.w
        self.y2 = self.h
        self.x1 = 0
        self.y1 = 0

    def multiply_by(self, value: int | float) -> None:
        self.x1 = round(self.x1 * value)
        self.y1 = round(self.y1 * value)
        self.x2 = round(self.x2 * value)
        self.y2 = round(self.y2 * value)

    def divide_by(self, value: int | float) -> None:
        self.x1 = round(self.x1 / value)
        self.y1 = round(self.y1 / value)
        self.x2 = round(self.x2 / value)
        self.y2 = round(self.y2 / value)

    def replace_from(self, bbox) -> None:
        assert isinstance(bbox, self.__class__)
        self.x1 = bbox.x1
        self.y1 = bbox.y1
        self.x2 = bbox.x2
        self.y2 = bbox.y2

    def update_from(self, bbox) -> None:
        assert isinstance(bbox, self.__class__)

        self.x1 = min(self.x1, bbox.x1)
        self.y1 = min(self.y1, bbox.y1)
        self.x2 = max(self.x2, bbox.x2)
        self.y2 = max(self.y2, bbox.y2)
