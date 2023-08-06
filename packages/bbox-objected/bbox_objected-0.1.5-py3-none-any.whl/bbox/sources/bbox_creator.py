from typing import Sequence, TypeVar

from ..types import BBoxKind


class BaseBBox:
    def __init__(self, coords: Sequence, kind: BBoxKind | str):
        kind = str(kind)
        assert kind in BBoxKind.__members__, f"Unacceptable bbox kind <{kind}>"

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        getattr(self, "_BaseBBox__create_" + kind)(coords)
        self.is_valid()

    def is_valid(self):
        comment = "Invalid coords passed, must be: x1({self.x1}) <= x2({self.x2}) and y1({self.y1}) <= y2({self.y2})"
        assert (self.x1 <= self.x2) and (self.y1 <= self.y2), comment

    def __create_pascal_voc(self, coords: Sequence) -> None:
        self.x1, self.y1, self.x2, self.y2 = coords

    def __create_x1y1x2y2(self, coords: Sequence) -> None:
        self.__create_pascal_voc(coords)

    def __create_coco(self, coords: Sequence) -> None:
        self.x1, self.y1 = coords[:2]
        self.x2, self.y2 = self.x1 + coords[2], self.y1 + coords[3]

    def __create_x1y1wh(self, coords: Sequence) -> None:
        self.__create_coco(coords)

    def __create_free_list(self, coords: Sequence) -> None:
        (self.x1, self.y1), (x2, y1), (self.x2, self.y2), (x1, y2) = coords

    def __create_tl_tr_br_bl(self, coords: Sequence) -> None:
        self.__create_free_list(coords)

    def __create_horizontal_list(self, coords: Sequence) -> None:
        self.x1, self.x2, self.y1, self.y2 = coords

    def __create_x1x2y1y2(self, coords: Sequence) -> None:
        self.__create_horizontal_list(coords)

    def __create_pywinauto(self, coords: Sequence) -> None:
        self.x1 = coords.left
        self.y1 = coords.top
        self.x2 = coords.right
        self.y2 = coords.bottom

    def __create_winocr(self, coords: dict[str, int | float]) -> None:
        self.x1, self.y1 = coords["x"], coords["y"]
        self.x2 = self.x1 + coords["width"]
        self.y2 = self.y1 + coords["height"]

    def __create_mss(self, coords: dict[str, int | float]) -> None:
        self.x1 = coords["left"]
        self.y1 = coords["top"]
        self.x2 = self.x1 + coords["width"]
        self.y2 = self.y1 + coords["height"]

    def __repr__(self):
        bbox = f"BBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        return f"<{bbox}>"


AnyBBox = TypeVar("AnyBBox", bound=BaseBBox)
