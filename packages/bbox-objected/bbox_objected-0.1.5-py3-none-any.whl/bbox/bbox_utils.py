import math
from contextlib import suppress

with suppress(ImportError):
    import numpy as np


from .sources.bbox_creator import AnyBBox, BaseBBox


def get_cos_between(bbox1: AnyBBox, bbox2: AnyBBox, xc: int | float, yc: int | float):
    v1 = np.array([bbox1.xc - xc, bbox1.yc - yc])
    v2 = np.array([bbox2.xc - xc, bbox2.yc - yc])

    inner = np.inner(v1, v2)
    norms = np.linalg.linalg.norm(v1) * np.linalg.linalg.norm(v2)

    cos = inner / norms
    return cos


def get_IoU(bbox_1: AnyBBox, bbox_2: AnyBBox):
    """Calculate Intersection over Union for two Bboxes"""
    try:
        assert hasattr(bbox_1, "area") and hasattr(
            bbox_2, "area"
        ), "one of sources doesn't have area attribute"
    except Exception as exc:
        if bbox_1 is None or bbox_2 is None:
            return 0
        raise exc

    x1 = max(bbox_1.x1, bbox_2.x1)
    y1 = max(bbox_1.y1, bbox_2.y1)
    x2 = min(bbox_1.x2, bbox_2.x2)
    y2 = min(bbox_1.y2, bbox_2.y2)

    inter_area = abs(max((x2 - x1, 0)) * max((y2 - y1), 0))
    if inter_area == 0:
        return 0

    return inter_area / (bbox_1.area + bbox_2.area - inter_area)


def sort_clockwise(bboxes: list, xc: float | int, yc: float | int):
    """Expect to get list of groups of BBoxes or list of BBoxes"""
    try:
        bboxes.sort(
            key=lambda group: math.atan2(group[-1].x2 - xc, group[-1].y1 - yc),
            reverse=True,
        )
    except TypeError:
        bboxes.sort(
            key=lambda group: math.atan2(group.x2 - xc, group.y1 - yc),
            reverse=True,
        )
    return bboxes


def get_distance(bbox_1: AnyBBox, bbox_2: AnyBBox):
    """Return distance between centers of BBox objects"""
    return math.dist(bbox_1.center, bbox_2.center)


def non_max_suppression(x1y1x2y2, thr: float) -> list[int | float]:
    if len(x1y1x2y2) == 0:
        return []

    if issubclass(x1y1x2y2[0], BaseBBox):
        x1y1x2y2 = np.array([bbox.get_pascal_voc() for bbox in x1y1x2y2])
    elif not isinstance(x1y1x2y2, np.ndarray):
        x1y1x2y2 = np.array(x1y1x2y2)

    # if the bounding x1y1x2y2 integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if x1y1x2y2.dtype.kind == "i":
        x1y1x2y2 = x1y1x2y2.astype("float")
    # initialize the list of picked indexes
    pick = []
    # grab the coordinates of the bounding x1y1x2y2
    x1 = x1y1x2y2[:, 0]
    y1 = x1y1x2y2[:, 1]
    x2 = x1y1x2y2[:, 2]
    y2 = x1y1x2y2[:, 3]
    # compute the area of the bounding x1y1x2y2 and sort the bounding
    # x1y1x2y2 by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)  # TODO: add sorting by area
    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > thr)[0])))
    # return only the bounding x1y1x2y2 that were picked using the
    # integer data type
    return pick
