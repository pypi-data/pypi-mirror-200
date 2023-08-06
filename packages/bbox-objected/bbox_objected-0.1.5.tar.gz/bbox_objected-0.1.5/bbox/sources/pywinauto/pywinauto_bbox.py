from .getter import PyWinAutoBBoxGetter
from ..bbox_img import BBoxImg


class PyWinAutoBBox(PyWinAutoBBoxGetter, BBoxImg):
    """
        Uses PyWinAuto for getting real coords of window during workflow
    Args:
        window - pywinauto object, must have .rectangle()
    """

    def __init__(self, window, text: str = "", **kwargs):
        self.window = window
        self.text = text
        self.__dict__.update(kwargs)

    def __repr__(self):
        bbox = self.window.rectangle()
        if text := self.text:
            text = f" - {self.text}"
        return f"<PyWinAutoBBox{bbox}{text}>"
