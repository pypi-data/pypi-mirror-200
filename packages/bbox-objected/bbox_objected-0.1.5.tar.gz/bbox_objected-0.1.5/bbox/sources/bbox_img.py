from abc import ABC
from contextlib import suppress

from ..cv_utils import resize

with suppress(ImportError):
    import cv2

with suppress(ImportError):
    import numpy as np


class BBoxImg(ABC):
    def show_on(self, img, text: str = ""):
        img = img.copy()
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        if (
            (0.0 <= self.x1 <= 1.0)
            and (0.0 <= self.y1 <= 1.0)
            and (0.0 <= self.x2 <= 1.0)
            and (0.0 <= self.y2 <= 1.0)
        ):
            h, w, *c = img.shape
            x1, y1, x2, y2 = self.as_abs(w, h).get_pascal_voc()
            cv2.rectangle(img, (round(x1), round(y1)), (round(x2), round(y2)), (0, 255, 0))
            cv2.putText(
                img,
                text,
                (round(x1), round(y1) + 10),
                cv2.FONT_ITALIC,
                0.5,
                (0, 0, 255),
                2,
            )
        else:
            cv2.rectangle(
                img, (round(self.x1), round(self.y1)), (round(self.x2), round(self.y2)), (0, 255, 0)
            )
            cv2.putText(
                img,
                text,
                (round(self.x1), round(self.y1) + 10),
                cv2.FONT_ITALIC,
                0.5,
                (0, 0, 255),
                2,
            )

        cv2.imshow("temp", resize(img, height=800))
        cv2.waitKey(0)
        cv2.destroyWindow("temp")

    def crop_from(self, img):
        if (
            (0.0 <= self.x1 <= 1.0)
            and (0.0 <= self.y1 <= 1.0)
            and (0.0 <= self.x2 <= 1.0)
            and (0.0 <= self.y2 <= 1.0)
        ):
            h, w, *c = img.shape
            x1, y1, x2, y2 = self.as_abs(w, h).get_pascal_voc()
            return img[y1:y2, x1:x2]
        else:
            img = img[self.y1 : self.y2, self.x1 : self.x2]

            return img
