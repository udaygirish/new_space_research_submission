# New_Space_Research_sampletask_sub
Repository for submitting the task for initial screening (Object Detection and Data gather and Vis)

###
* Before executing or running the script please use 
"sudo pip3 install -r requirements.txt" in your terminal.
* To evaluate the output please run  bash test_script.sh in your terminal
* Current Net AVG IOU for center net model is 0.659 (without considering missing detections)
* Current NET AVG IOU for centeer net model is 0.604(with considering missing detections)
* Current Net AVG IOU for efficientdet model is 0.797 (without considering missing detections)
* Current NET AVG IOU for efficientdet model is 0.365 (with considering missing detections)
* It is truly evident that from the results center net is able to give more detections considering the 0.35 threshold than efficientdet v7 on this particular image. But there might be other models which might give good accuracy on this image but more exploration is not done as one image evaluation wont give any inference.
* But for the sake of experimentation YOLO v4 is tested and the output is present as output/yolo_predictions.jpg but the score is not calculated as yolo is not involved to work with this script - can be done needs more time.
* Real reason of going with Center net is because of its keypoint estimation capability which can help in aerial imagery to monitor people more effectively if the stream is of high resolution.

### This Branch is for object detection(Person) task on a single image (Aerial View)
<ul>
<li> This script currently works on pretrained model alone. </li>
<li> Because of the above reason the average IOU might be less as the detections are less </li>
<li> The average doesn't account take of the missing detections as IoU is not a true measure of accuracy so another average named avg_wd which considers the missing detections and reports based on ground truth </li>
<li> This script downloads two models Centre Net Hour glass 1024^2 which is intuitively best model for distant short object detection and Efficient Det model v7 which is having the highest mAP and the current SOTA in most of the use cases </li>
<li> The model_download script downloads almost 1 gb data so if user wants to test other model shorter or something please visit tensorflow hub models to get your wanted model and place the model files such as assets,variables, saved_model.pb in the model folder </li>
<li> Yolov4 is also good for this task but it doesn't make sense to use that directly and build as still it is just modifying darknet.py script </li>
<li> There is a video inference script also provided if it is needed to run on a video but it uses ffmpeg please install by executing sudo apt-get install ffmpeg and then run video_inference.sh </li>
<li> There is a benchmark function but it is not included in current script execution but this helps to benchmark FPS </li>
</ul>

***

### The below  arguments helps you to run the script 
* Even though a predefined script is there for the best model center net to just validate code the below arguments are for models outside what I haven't downloaded and configured.

#### <u>Arguments</u>
***
* -i to specify image path (Just specify image folder the script is capable of rendering output for all images placed in the folder) (Needed Arg)
* -mp to specify model path (Currently if you have executed model_download.sh it can work by taking input namely ./models/centernet_hourglass_1024 and ./models/efficientdet_d7
* -o to specify output path (currently set to ./output/)
* -ci to specify whether to calculate avg iou or not (currently set to True)
* -b to specify benchmark currently this func is not completely configured to run with main code 

***
* For  running video inference please use video_inference.sh
* arguments for the script / how to execute the script 
* <video_name>
* <frame_rate>
* <model_path>
* <any no (run no or version no)>
* Sample execution: bash video_inference.sh test.mp4 4 ./model/centernet_hourglass_1024 run1 
* It creates test_run1.mp4

### Limitations
* At present, while running the script there are some layer loading warnings from tensorflow but still the script works perfectly please ignore the warnings the final output is still perfect (This might be observed depending on tf version) - these are removed by setting the tf env logger to mode 3 which is ERROR only.
* Small models are tried but havent included in the final results because the results are poor with them as this image is large in terms of frame size.

### Future scope
* Results can be improved by training the model using pretrained weights and then hyperparameter tuning but that needs both time and resources.
* Model inference can be made faster by hosting the backend as tensorflow-serving or TensorRT or using deepstream if used for edge devices.
* Model size and a small significant improvement in latency can be observed if model is pruned and quantized to int8 or  mixed precision.
* Deploying on Edge devices if drones are used by using People net kind models with the help of deepstream and transfer learning toolkit which can give a boost on both FPS and model memory occupancy and mAP.


*** 
For any quries please contact einsteingirish@gmail.com , 
Ph.No : 8137080271

My Website: https://udaygirish.github.io/

