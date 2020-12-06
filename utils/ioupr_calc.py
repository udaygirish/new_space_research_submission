'''
Function to calculate Precision, Recall, F-Score, 
IOU by taking the given groundtruth xml file from 
the same location as the image
'''
from .eval import parse_single_file as ps
import numpy as np
from scipy.spatial import distance

class IOU_PR_Calc():
    def __init__(self):
        self.data = None
    
    def bbox_gc_conv(self,bbox_coord,class_ids):
        bbox_total_list = []
        for i in range(len(bbox_coord)):
            k = bbox_coord[i]
            j = class_ids[i]
            if j == 1:
                temp_id = 'person'
            temp_list = [temp_id,k[0],k[1],k[2],k[3]]
            bbox_total_list.append(temp_list)
        return bbox_total_list
    
    def bbox_pc_conv(self,bbox_coord):
        bbox_total_list = []
        for i in range(len(bbox_coord)):
            k = bbox_coord[i][1:]
            j = bbox_coord[i][0]
            temp_list = [j,k[0],k[1],k[2]+k[0],k[3]+k[1]]
            bbox_total_list.append(temp_list)
        return bbox_total_list

    def find_centroid_and_append(self,bbox_list):
        bbox_updated_dict ={}
        count = 0
        for i in bbox_list:
            center_coord =  (i[1]+(i[3]/2), i[2]+(i[4]/2))
            bbox = [i[1],i[2],i[3],i[4]]
            temp_cn = i[0]
            temp = [center_coord,temp_cn,bbox]
            bbox_updated_dict[count] = temp
            count = count+1
        return bbox_updated_dict
    
    def iou_calc(self,box1,box2):
        # determine the (x, y)-coordinates of the intersection rectangle
        xA = max(box1[0], box2[0])
        yA = max(box1[1], box2[1])
        xB = min(box1[2], box2[2])
        yB = min(box1[3], box2[3])
        # compute the area of intersection rectangle
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
        # compute the area of both the prediction and ground-truth
        # rectangles
        boxAArea = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
        boxBArea = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interArea / float(boxAArea + boxBArea - interArea)
        # return the intersection over union value
        return iou

    def find_euclidean_distance(self,tuple1,tuple2):
        dist = distance.euclidean(tuple1, tuple2)
        return dist

    def associate_keys_calc_iou(self,dict1,dict2):
        associated_keys = []
        associated_iou = []
        for i in dict1.keys():
            temp_dist_list = []
            temp_iou_list = []
            for j in dict2.keys():
                temp_euc_dist = round(self.find_euclidean_distance(dict1[i][0],dict2[j][0]),2)
                temp_iou = self.iou_calc(dict1[i][2],dict2[j][2])
                temp_dist_list.append(temp_euc_dist)
                temp_iou_list.append(temp_iou)
            max_iou_index = temp_iou_list.index(max(temp_iou_list))
            min_dist_index = temp_dist_list.index(min(temp_dist_list))
            if max_iou_index == min_dist_index:
                associated_keys.append(min_dist_index)
                associated_iou.append(temp_iou_list[max_iou_index])
            else:
                associated_keys.append(min_dist_index)
                associated_iou.append(temp_iou_list[min_dist_index])
        return associated_keys,associated_iou
    
    def _compute_iou(self,image_path,detections):
        self.xml_path = "./"+image_path.split(".")[-2]+".xml"
        self.bbox_coord, self.class_ids,self.size_list = ps("./",self.xml_path)
        self.bbox_coord = self.bbox_coord.tolist()
        length_gc_coord = len(self.bbox_coord)
        length_pc_coord = len(detections)
        self.detections = detections
        self.bbox_gc_coord = self.bbox_gc_conv(self.bbox_coord,self.class_ids)
        self.bbox_pc_coord = self.bbox_pc_conv(self.detections)

        self.bbox_gc_dict = self.find_centroid_and_append(self.bbox_gc_coord)
        self.bbox_pc_dict = self.find_centroid_and_append(self.bbox_pc_coord)
        self.ass_keys, self.ass_iou = self.associate_keys_calc_iou(self.bbox_pc_dict,self.bbox_gc_dict)
        #print("IOU_LIST:{}, ASSOCIATED_BOX_LIST:{}".format(self.ass_iou,self.ass_keys))
        return self.ass_iou, self.ass_keys,length_gc_coord,length_pc_coord
    

 

def compute_avg_iou(image_path,detections,threshold):
    iou_calc = IOU_PR_Calc()
    ass_iou,ass_keys, l_gc_coord,l_pc_coord = iou_calc._compute_iou(image_path,detections)
    ass_iou = [i for i in ass_iou if i>threshold]
    avg_sum = np.sum(ass_iou)
    avg_iou = round(avg_sum/l_pc_coord,3)
    avg_w_iou = round(avg_sum/l_gc_coord,3)
    print("-------------------------------------------------------------------")
    print("-------------------------------------------------------------------")
    print("THE AVERAGE IOU without undetected entities is :{}".format(avg_iou))
    print("The AVERAGE IOU with undetected entities is :{}".format(avg_w_iou))
    print("-------------------------------------------------------------------")
    print("-------------------------------------------------------------------")
