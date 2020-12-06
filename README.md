# New_Space_Research_sampletask_sub
Repository for submitting the task for initial screening (Object Detection and Data gather and Vis)

###
* Before executing or running the script please use 
"sudo pip3 install -r requirements.txt" in your terminal.
* To evaluate the output please run  bash test_script.sh in your terminal

### This Branch is for object detection(Person) task on a single image (Aerial View)
<ul>
<li> This script currently works on pretrained model alone. </li>
<li> Because of the above reason the average IOU might be less as the detections are less </li>
<li> The average doesn't account take of the missing detections as IoU is not a true measure of accuracy so another average named avg_wd which considers the missing detections and reports based on ground truth </li>
<li> This script downloads two models Centre Net Hour glass 1024^2 which is intuitively best model for distant short object detection and Efficient Det model v7 which is having the highest mAP and the current SOTA in most of the use cases </li>
<li> The model_download script downloads almost 1 gb data so if you want to test other model shorter or something please visit tensorflow hub models to get your wanted model and place the model files such as assets,variables, saved_model.pb in the model folder </li>
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
* At present, while running the script there are some layer loading warnings from tensorflow but still the script works perfectly please ignore the warnings the final output is still perfect (This might be observed depending on tf version).


*** 
For any quries please contact einsteingirish@gmail.com , 
Ph.No : 8137080271

My Website: https://udaygirish.github.io/

