import tensorflow as tf
import os
import cv2
import numpy as np

# Grab path to current working directory
CWD_PATH = os.getcwd()
# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = 'outhers/frozen_inference_graph.pb'
# Path to label map file
PATH_TO_LABELS = 'outhers/label_map.pbtxt'
# Number of classes the object detector can identify
NUM_CLASSES = 1

# Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
#category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    sess = tf.compat.v1.Session(graph=detection_graph)
    
def trat_detect_objet_extract (input_image):

    # Define input and output tensors (i.e. data) for the object detection classifier
    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Load image using OpenCV and
    # expand image dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value

    #input_image=cv2.resize(input_image,(500,500))
    image_expanded = np.expand_dims(input_image, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],feed_dict={image_tensor: image_expanded})

    quant_boxes = len(scores[scores > 0.4])
    
    list_images = []
    contador = 0
    for box in boxes[0,:quant_boxes]:
        (height, width) = input_image.shape[:2]
        ymin = int((boxes[0][contador][0]*height)*0.9)
        xmin = int((boxes[0][contador][1]*width)*0.9)
        ymax = int((boxes[0][contador][2]*height)*1.1)
        xmax = int((boxes[0][contador][3]*width)*1.1)
        img = np.array(input_image[ymin:ymax,xmin:xmax])

        #Resize
        img=cv2.resize(img,(500,500))
        img=img.astype('float32')
        img=img.reshape(500,500,3)
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        list_images.append(img)
        contador = contador + 1

    return list_images
    
    