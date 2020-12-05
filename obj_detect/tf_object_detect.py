import tensorflow.compat.v1 as tf1
import tensorflow as tf
import cv2
import json
import numpy as np

np.random.seed(0)

class ObjectDetection(object):
    def __init__(self, saved_model_dir_or_frozen_graph):
        """Initialize the inference driver.
        Args:
          saved_model_dir_or_frozen_graph: checkpoint path, such as /tmp/efficientdet-d0/
          model_type: efficientdet or ssd model or any other pretrained model
          filter_classes: the classnames for filtering predictions..
          use_xla: Whether run with xla optimization.
          threshold: minimal score threshold for filtering predictions.
        """

        self.signatures = None
        self.sess = None
        with open('config/label_map.json') as json_file:
            self.idx2label = json.load(json_file, object_hook=lambda d: {int(k): v for k, v in d.items()})
            
        with open('config/idx2color.json') as json_file:
            idx2color = json.load(json_file, object_hook=lambda d: {int(k): v for k, v in d.items()})
            
        self.label2color = { v: tuple(idx2color[k]) for k, v in self.idx2label.items()}
        
        with open('config/config.json') as json_file:
            data = json.load(json_file)
            self.threshold = data.get("min_conf_threshold", 0.)
            self.filter_classes = data.get("filter_classes", [])
            self.model_type = data.get("model_type", "other_tf_od")
            self.model_format = data.get("model_format", "x1y1x2y2")

        self.detect_fn = self.load(saved_model_dir_or_frozen_graph)

        if self.model_type == "efficientdet":
            self.signatures = {
                'image_files': 'image_files:0',
                'image_arrays': 'image_arrays:0',
                'prediction': 'detections:0',
            }
        else:
            # build tensor dict
            image_tensor = 'image_tensor:0'
            
            #image_tensor = 'image_tensor:0'
            boxes = 'detection_boxes:0'
            scores = 'detection_scores:0'
            classes = 'detection_classes:0'
            num_detections = 'num_detections:0'

            self.signatures = {
                'image_arrays': image_tensor,
                'prediction': [boxes, scores, classes, num_detections],
            }


    def _build_session(self):
        sess_config = tf1.ConfigProto()
        return tf1.Session(config=sess_config)

    def load(self, saved_model_dir_or_frozen_graph):
        """Load the model using saved model or a frozen graph."""
        if self.model_type == "tf2_od":
            return tf.saved_model.load(export_dir=saved_model_dir_or_frozen_graph)
            
        if not self.sess:
            self.sess = self._build_session()

        # Load saved model if it is a folder.
        if tf1.io.gfile.isdir(saved_model_dir_or_frozen_graph):
            return tf1.saved_model.load(self.sess, ['serve'], saved_model_dir_or_frozen_graph)

        # Load a frozen graph.
        graph_def = tf1.GraphDef()
        with tf1.gfile.GFile(saved_model_dir_or_frozen_graph, 'rb') as f:
            graph_def.ParseFromString(f.read())
        tf1.import_graph_def(graph_def, name='')


    def predict(self, image_arrays):
        """Serve a list of image arrays.
        Args:
          image_arrays: A list of image content with each image has shape [height, width, 3] and uint8 dtype.
        Returns:
          A list of detections.
        """
        filtered_detections = []
        if self.model_type == "tf2_od":
            output_dict = self.detect_fn(image_arrays)
            img_h, img_w, img_ch = image_arrays[0].shape
            predictions= [output_dict['detection_boxes'], output_dict['detection_scores'], output_dict['detection_classes'], output_dict['num_detections']]
            filtered_detections = self.format_tf_od_predictions(predictions, img_h, img_w, self.threshold,
                                                                self.filter_classes)
        
        elif self.model_type == "efficientdet":
            predictions = self.sess.run(self.signatures['prediction'],
                                    feed_dict={self.signatures['image_arrays']: image_arrays})
            print("Length of raw preds:", len(predictions[0]))
            print("Raw preds:", predictions[0])
            filtered_detections = self.format_effnet_predictions(predictions[0], self.threshold, self.filter_classes)
        else:
            predictions = self.sess.run(self.signatures['prediction'],
                                    feed_dict={self.signatures['image_arrays']: image_arrays})
            img_h, img_w, img_ch = image_arrays[0].shape
            filtered_detections = self.format_tf_od_predictions(predictions, img_h, img_w, self.threshold,
                                                                self.filter_classes)
        return filtered_detections

    def format_tf_od_predictions(self, predictions, img_h, img_w, threshold, filter_classes = []):
        (boxes, scores, classes, num_detections) = predictions
        boxes = boxes[0]
        scores = scores[0]
        classes = classes[0]
        num_detections = num_detections[0]

        detections = []
        for i in range(int(num_detections)):
            score = scores[i]
            obj_class = self.idx2label.get(int(classes[i]),"other")
            if score >= threshold:
                if (len(filter_classes) >= 1 and obj_class in filter_classes) or len(filter_classes) == 0:
                    y1, x1, y2, x2 = boxes[i]
                    y1_o = y1 * img_h
                    x1_o = x1 * img_w
                    y2_o = y2 * img_h
                    x2_o = x2 * img_w
                    if self.model_format == "x1y1x2y2":
                        x = x1_o
                        y = y1_o
                        w = x2_o - x1_o
                        h = y2_o - y1_o
                    else:
                        x = x1_o
                        y = y1_o
                        w = x2_o
                        h = y2_o
                    detections.append([obj_class, int(x), int(y), int(w), int(h),round(float(score),2) ])

        return detections


    def format_effnet_predictions(self, predictions, threshold, filter_classes = []):
        # each detection has a format [image_id, y, x, height, width, score, class]
        detections = []
        for detection in predictions:
            _, y, x, h, w, score, class_id = detection
            obj_class = self.idx2label.get(int(class_id),"other")
            if score >= threshold:
                if (len(filter_classes) >= 1 and obj_class in filter_classes) or len(filter_classes) == 0:
                    detections.append([obj_class, int(x), int(y), int(w), int(h) ])
        return detections


if __name__ == "__main__":
    print("tf version:", tf1.__version__)
    saved_model_dir = "models/ssd_mobilenet_fpn/ssd_mobilenet_fpn_frozen.pb"
    image_path_pattern = "test_data/img1.jpg"
    obj_det = ObjectDetection(saved_model_dir)
    # Serving time batch size should be fixed.
    all_files = list(tf1.io.gfile.glob(image_path_pattern))
    print('all_files=', all_files)
    raw_images = cv2.imread(all_files[0])
    detections_bs = obj_det.predict([raw_images])
    print("Detections:",detections_bs)
