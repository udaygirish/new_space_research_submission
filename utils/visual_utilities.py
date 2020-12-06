import cv2
import numpy as np


def overlay_bbox(frame, bbox_base, color_bbox, conf=1, show_txt=True):
    """Overlays bounding boxes on the frame
    Parameters
    ----------
    frame (numpy array): numpy array input frame
    bbox (list): list of detection bounding box coordinates
    color_bbox (dict): to identify which color the bbox based must be overlayed based on the category
    conf (float): confidence score of the detection

    Return type
    -----------
    -
    """
    bbox = np.array(bbox_base[1:-1], dtype=np.int32)
    cat = bbox_base[0]
    score = bbox_base[-1]
    printable_text = cat + "_" + str(score)
    c = color_bbox.get(cat, (0, 120, 255))
    font = cv2.FONT_HERSHEY_SIMPLEX
    cat_size = cv2.getTextSize(cat, font, 0.5, 2)[0]
    cv2.rectangle(
        frame, (bbox[0], bbox[1]), (bbox[2] + bbox[0], bbox[3] + bbox[1]), c, 2
    )
    if show_txt:
        # cv2.rectangle(frame,
        #              (bbox[0], bbox[1] - cat_size[1] - 2),
        #              (bbox[0] + cat_size[0], bbox[1] - 2), c, -1)
        cv2.putText(
            frame,
            printable_text,
            (bbox[0], bbox[1] - 2),
            font,
            0.3,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
