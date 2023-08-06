from abc import ABC

from ...types import BBoxKind


class PyWinAutoBBoxGetter(ABC):
    @property
    def x1(self):
        return self.window.rectangle().left

    @property
    def x2(self):
        return self.window.rectangle().right

    @property
    def y1(self):
        return self.window.rectangle().top

    @property
    def y2(self):
        return self.window.rectangle().bottom

    def get(self, kind: BBoxKind | str) -> tuple:
        return getattr(self, "get_" + str(kind))()

    def get_pascal_voc(self) -> tuple[int, int, int, int]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return x1, y1, x2, y2

    def get_x1y1x2y2(self) -> tuple[int, int, int, int]:
        return self.get_pascal_voc()

    def get_coco(self) -> tuple[int, int, int, int]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return x1, y1, x2 - x1, y2 - y1

    def get_x1y1wh(self) -> tuple[int, int, int, int]:
        return self.get_coco()

    def get_free_list(
        self,
    ) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return (x1, y1), (x2, y1), (x2, y2), (x1, y2)

    def get_tl_tr_br_bl(
        self,
    ) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        return self.get_free_list()

    def get_horizontal_list(self) -> tuple[int, int, int, int]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return x1, x2, y1, y2

    def get_x1x2y1y2(self) -> tuple[int, int, int, int]:
        return self.get_horizontal_list()

    def get_mss(self) -> dict[str, int]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}

    @property
    def w(self) -> int:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return x2 - x1

    @property
    def h(self) -> int:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return y2 - y1

    @property
    def xc(self) -> int | float:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return (x1 + x2) / 2

    @property
    def yc(self) -> int | float:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return (y1 + y2) / 2

    @property
    def area(self) -> int:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return (x2 - x1) * (y2 - y1)

    @property
    def center(self) -> tuple[int | float, int | float]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return (x1 + x2) / 2, (y1 + y2) / 2

    @property
    def tl(self) -> tuple[int, int]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return x1, y1

    @property
    def tr(self) -> tuple[int, int]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return x2, y1

    @property
    def br(self) -> tuple[int, int]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return x2, y2

    @property
    def bl(self) -> tuple[int, int]:
        x1, y1, x2, y2 = self.__get_raw_coords()
        return x1, y2

    def __get_raw_coords(self) -> tuple[int, int, int, int]:
        rect = self.window.rectangle()
        return rect.left, rect.top, rect.right, rect.bottom
