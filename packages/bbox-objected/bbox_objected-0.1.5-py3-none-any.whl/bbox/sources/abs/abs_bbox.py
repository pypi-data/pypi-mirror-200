from typing import Sequence

from .editor import AbsBBoxEditor
from ..bbox_img import BBoxImg
from ...types import BBoxKind


class AbsBBox(AbsBBoxEditor, BBoxImg):
    def __init__(
        self,
        coords: Sequence,
        kind: BBoxKind | str = "x1y1x2y2",
        text: str = "",
        **kwargs,
    ):
        super().__init__(coords, kind)
        self.is_valid()
        self.text = text
        self.__dict__.update(kwargs)

    def is_valid(self):
        comment = "Use only int coords"
        return (
            isinstance(self.x1, int)
            and isinstance(self.y1, int)
            and isinstance(self.x2, int)
            and isinstance(self.y2, int),
            comment,
        )

    def as_rel(self, img_w: int, img_h: int):
        from ..rel.rel_bbox import RelBBox

        x1, y1, x2, y2 = self.get_pascal_voc()
        x1 = x1 / img_w
        y1 = y1 / img_h
        x2 = x2 / img_w
        y2 = y2 / img_h
        return RelBBox((x1, y1, x2, y2), text=self.text)

    def __repr__(self):
        bbox = f"AbsBBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        if text := self.text:
            text = f" - {self.text}"
        return f"<{bbox}{text}>"
