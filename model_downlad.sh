echo "For Now the best models are only getting downloaded"
echo "In terms of performance (Latency,mAP) and some intuition"

wget https://tfhub.dev/tensorflow/efficientdet/d7/1?tf-hub-format=compressed -O efficientdet_d7_1.tar.gz
echo "Efficient Det v7 downloaded(COCO mAP:51.2 , Latench: 325 ms)"
echo "Extracting ..."
mkdir -p ./models/efficientdet_d7/
tar -xvf efficientdet_d7_1.tar.gz --directory ./models/efficientdet_d7/
echo "Extraction Completed"
wget https://tfhub.dev/tensorflow/centernet/hourglass_1024x1024/1?tf-hub-format=compressed -O centernet_hourglass_1024x1024_1.tar.gz
echo "Center Net Hourglass_1024*1024 downloaded (COCO mAP : 44.5 , Latency: 197 ms)"
echo "Extracting ...."
mkdir -p ./models/centernet_hourglass_1024/
tar -xvf centernet_hourglass_1024x1024_1.tar.gz --directory ./models/centernet_hourglass_1024/
echo "Extraction Completed."
echo "------------------------------------------------------------------------------------"
echo "Removing tar files..."
rm -r *.tar.gz
echo "Model download completed"