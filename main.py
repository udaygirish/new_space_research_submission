import cv2
from obj_detect.tf_object_detect import ObjectDetection
from time import time
from utils.visual_utilities import overlay_bbox
import argparse
import os
import glob
from tqdm import tqdm
import numpy as np
from utils.ioupr_calc import compute_avg_iou
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def get_output_paths(input_paths, target_dir):
    output_paths = []
    for inp_pth in input_paths:
        head, tail = os.path.split(inp_pth)
        fname, ext = tail.split(".")
        full_path = os.path.join(target_dir, fname+"_output."+ext)
        output_paths.append(full_path)
    return output_paths

def main(): 
    
    parser = argparse.ArgumentParser()  
    parser.add_argument("-mp", "--model_path", required=True, help = "saved model path (folder name) or frozen graph file path") 
    parser.add_argument("-i", "--image_path", required=True, help = "Image path") 
    parser.add_argument("-o", "--output_path", default="output", help="output image path")
    #parser.add_argument("-b", "--benchmark", action='store_true', help="Do benchmark")
    parser.add_argument("-ci","--iou_calc",default=True,help="To specify whether to calculate mAP or not")
    args = parser.parse_args() 
    
    os.makedirs(args.output_path, exist_ok=True)
    saved_model_dir_or_fg = args.model_path
    obj_det = ObjectDetection(saved_model_dir_or_fg)
    
    if os.path.isdir(args.image_path):
        file_types = ('*.jpeg','*.jpg', '*.png')
        file_paths = []
        for f_type in file_types:
            file_paths.extend(glob.glob(os.path.join(args.image_path, f_type)))
    else:
        file_paths = [args.image_path]
        
    output_paths = get_output_paths(file_paths, args.output_path)
    print("Input File paths:", file_paths[0])
    print("output paths:", output_paths[0])
    
    for i, img_path in tqdm(enumerate(file_paths)):
        original_image = cv2.imread(img_path)
        #original_image = cv2.resize(original_image,(1024,1024))
        detections = obj_det.predict([original_image])
        for bbox in detections:            
            overlay_bbox(original_image, bbox, obj_det.label2color)
        print(len(detections))
        iou_threshold=0.0
        if args.iou_calc==True:
            compute_avg_iou(img_path,detections,iou_threshold)
        else:
            pass
        cv2.imwrite(output_paths[i], original_image)
    

def benchmark():
    saved_model_dir_or_fg = "models/ssd_mobilenet_fpn/ssd_mobilenet_fpn_frozen.pb"
    original_image = cv2.imread("test_data/TopDownHumanDetection_4032x3024")
    obj_det = ObjectDetection(saved_model_dir_or_fg)

    # warm-up
    for _ in range(5):
        obj_det.predict([original_image])

    # actual
    iterations = 100
    stime = time()
    for _ in range(iterations):
        obj_det.predict([original_image])

    etime = time()
    total_time = etime - stime
    avg_time_per_image = total_time/iterations
    print("Total time:", total_time, "for iterations:",iterations)
    print("Average time per image:", avg_time_per_image)
    print("FPS:", 1/avg_time_per_image)


if __name__ == "__main__":
    main()
