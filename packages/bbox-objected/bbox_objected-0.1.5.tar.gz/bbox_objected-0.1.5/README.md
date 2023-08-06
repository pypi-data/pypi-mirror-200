# bbox-objected

---

Makes manipulations with bounding boxes easier in Computer Vision projects. With zero dependencies by default.

---

## Installation:

`pip install bbox-objected`

### Optional dependencies:

`pip install numpy`

`pip install opencv-python` or `pip install opencv-contrib-python`

## Examples:
`AbsBBox` is needed to store absolute coordinates (uses `int` type strictly)
```python
from bbox import AbsBBox

bbox = AbsBBox((35, 45, 100, 80), kind="coco", text="abs_sample")

print(bbox)
# <AbsBBox(x1=35, y1=45, x2=135, y2=125) - abs_sample>

print(bbox.get_pascal_voc()) # you can get coords in specific formats
# (35, 45, 135, 125)
```
If you need to store relative coordinates, you can use `RelBBox` (values in range [0., 1.])
```python
from bbox import RelBBox

bbox = RelBBox((0.1, 0.2, 0.5, 0.6), kind="horizontal_list", text="rel_sample")

print(bbox)
# <RelBBox(x1=0.1, y1=0.5, x2=0.2, y2=0.6) - rel_sample>

print(bbox.get_free_list())
# ((0.1, 0.5), (0.2, 0.5), (0.2, 0.6), (0.1, 0.6))
```
Conversion between types is available
```python
from bbox import RelBBox

bbox = RelBBox((0.1, 0.2, 0.5, 0.6), kind="pascal_voc", text="sample")

print(bbox)
# <RelBBox(x1=0.1, y1=0.2, x2=0.5, y2=0.6) - sample>

print(bbox.as_abs(1920, 1080))  # size of image is necessary for conversion
# <AbsBBox(x1=192, y1=216, x2=960, y2=648) - sample>

print(bbox.as_abs(1920, 1080).as_rel(1920, 1080)) # each conversion creates new instance
# <RelBBox(x1=0.1, y1=0.2, x2=0.5, y2=0.6) - sample>
```
There is a bunch of attributes for each bbox
```python
from bbox import RelBBox, AbsBBox

bbox = RelBBox((0.4, 0.4, 0.6, 0.6))

print(bbox.x1, bbox.y1, bbox.x2, bbox.y2)
#  0.4 0.4 0.6 0.6
print(bbox.w, bbox.h)
#  0.2 0.2
print(bbox.tl, bbox.tr, bbox.br, bbox.bl)  # corners
#  (0.4, 0.4) (0.6, 0.4) (0.6, 0.6) (0.4, 0.6)

bbox = AbsBBox((40, 40, 60, 60))

print(bbox.center, bbox.area)
#  (50.0, 50.0) 400
print(bbox.xc, bbox.yc)
#  50.0 50.0
```
Available _**kinds**_ of bboxes:
```python
from bbox.types import BBoxKind

BBoxKind.free_list = "tl_tr_br_bl"  # special format of 'EasyOCR' library
BBoxKind.tl_tr_br_bl = "tl_tr_br_bl"
BBoxKind.horizontal_list = "x1x2y1y2"  # special format of 'EasyOCR' library
BBoxKind.x1x2y1y2 = "x1x2y1y2"
BBoxKind.pascal_voc = "x1y1x2y2"  # own format of PascalVOC image dataset
BBoxKind.x1y1x2y2 = "x1y1x2y2"
BBoxKind.coco = "x1y1wh"  # own format of COCO image dataset
BBoxKind.x1y1wh = "x1y1wh"
BBoxKind.pywinauto = "pywinauto"  # gets object of '.rectangle()' method of 'PyWinAuto' library
BBoxKind.winocr = "winocr"  # gets special coords format of 'WinOCR' library
BBoxKind.mss = "mss"  # gets 'monitor' object of library 'mss'
```
There is respective `get_` method for each bbox _**kind**_, except `"pywinauto"` and `"winocr"`

Some simple editing of bboxes is also available
```python
from bbox import AbsBBox

bbox = AbsBBox((100, 200, 300, 400))

print(bbox)
#  <AbsBBox(x1=100, y1=200, x2=300, y2=400)>
bbox.zero_basis()
print(bbox)
#  <AbsBBox(x1=0, y1=0, x2=200, y2=200)>
bbox.move_basis(25, 45)
print(bbox)
#  <AbsBBox(x1=25, y1=45, x2=225, y2=245)>

other_bbox = AbsBBox((200, 300, 400, 500))

print(other_bbox)
#  <AbsBBox(x1=200, y1=300, x2=400, y2=500)>
bbox.update_from(other_bbox)  # choose coords to get max area, don't create new instance
print(bbox)
#  <AbsBBox(x1=25, y1=45, x2=400, y2=500)>
bbox.replace_from(other_bbox)  # takes all coords from 'other', don't create new instance
print(bbox)
#  <AbsBBox(x1=200, y1=300, x2=400, y2=500)>
```


## Additional functionality:
Each bbox can be drawn or cropped from image. Can work both with `AbsBBox` and `RelBBox`

```python
import numpy as np

from bbox import AbsBBox

bbox = AbsBBox((100, 200, 300, 400))  # 'pascal_voc' bbox kind is default

img = np.empty((512, 512, 3), dtype=np.uint8)  # random RGB image

cropped = bbox.crop_from(img)  # 'numpy' must be installed
print(cropped.shape)
# (200, 200, 3)

bbox.show_on(img, text="sample")  # 'opencv' must be installed
```
Also, there are several useful functions. Currently works only with `AbsBBox`.

```python
from bbox import AbsBBox
from bbox.bbox_utils import get_distance, get_IoU, get_cos_between

bbox_1 = AbsBBox((100, 200, 300, 400), kind="x1y1wh")
bbox_2 = AbsBBox((100, 400, 100, 400), kind="horizontal_list")

print(get_distance(bbox_1, bbox_2))
#  150.0
print(get_IoU(bbox_1, bbox_2))  # Intersection over Union (ratio of intersection)
#  0.4
print(get_cos_between(bbox_1, bbox_2, 450, 350))  # angle around center in (450 ,350)
#  0.7592566023652966

```

```python
import numpy as np

from bbox.cv_utils import resize

img = np.empty((512, 512, 3), dtype=np.uint8)
resized = resize(img, height=128)  # aspect ratio will be saved

print(resized.shape)
# (128, 128, 3)
```