from enum import Enum


class BBoxKind(Enum):
    free_list = "tl_tr_br_bl"
    tl_tr_br_bl = "tl_tr_br_bl"
    horizontal_list = "x1x2y1y2"
    x1x2y1y2 = "x1x2y1y2"
    pascal_voc = "x1y1x2y2"
    x1y1x2y2 = "x1y1x2y2"
    coco = "x1y1wh"
    x1y1wh = "x1y1wh"
    pywinauto = "pywinauto"
    winocr = "winocr"
    mss = "mss"

    def __str__(self):
        return self.name
