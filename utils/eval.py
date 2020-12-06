import os
import numpy as np
import xml.etree.ElementTree as ET
import glob


def parse_single_file(dir_path, filename):
    global label2idx
    label2idx = {"Person": 1}
    xml = open(os.path.join(dir_path, filename), "r")
    # print(xml)
    tree = ET.parse(xml)
    root = tree.getroot()
    xml_size = root.find("size")
    size = {
        "width": xml_size.find("width").text,
        "height": xml_size.find("height").text,
        "depth": xml_size.find("depth").text,
    }

    objects = root.findall("object")
    if len(objects) == 0:
        return False, "number object zero"

    class_ids = []
    bbox_coord = []

    for _object in objects:
        if not _object.find("name").text in label2idx.keys():
            continue
        tmp = {"name": _object.find("name").text}

        xml_bndbox = _object.find("bndbox")
        bndbox = {
            "xmin": float(xml_bndbox.find("xmin").text),
            "ymin": float(xml_bndbox.find("ymin").text),
            "xmax": float(xml_bndbox.find("xmax").text),
            "ymax": float(xml_bndbox.find("ymax").text),
        }
        class_ids.append(label2idx[tmp["name"]])
        w = bndbox["xmax"] - bndbox["xmin"]
        h = bndbox["ymax"] - bndbox["ymin"]
        bbox_coord.append(
            [bndbox["xmin"], bndbox["ymin"], bndbox["xmax"], bndbox["ymax"]]
        )  # x1, y1, x2, y2
    size_list = [size["width"], size["height"]]
    bbox_coord = np.array(bbox_coord)
    class_ids = np.array(class_ids)
    return bbox_coord, class_ids, size_list


all_files = list(glob.glob("test_data/images/*.jpg"))
