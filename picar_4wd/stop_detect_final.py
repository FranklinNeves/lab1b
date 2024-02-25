import cv2
import sys
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from tflite_support.task import vision
from tflite_support.task import processor
from tflite_support.task import core
import utils_detect  
import picar_4wd as fc

# Initialize PiCamera
camera = PiCamera()
camera.resolution = (640, 480)  # Adjust resolution to your needs
camera.framerate = 2
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)  # Allow the camera to warm up

# Define the model, change these parameters according to your model and requirements
model_path = "efficientdet_lite0.tflite"  # Update this to the path of your model
enable_edgetpu = False  # Set to True if using Coral Edge TPU
num_threads = 2  # Adjust based on your system's capabilities

# Initialize the object detection model
base_options = core.BaseOptions(file_name=model_path, use_coral=enable_edgetpu, num_threads=num_threads)
detection_options = processor.DetectionOptions(max_results=3, score_threshold=0.3)
options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
detector = vision.ObjectDetector.create_from_options(options)

# Variables to calculate FPS
counter, fps = 0, 0
start_time = time.time()
fps_avg_frame_count = 10

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    image = cv2.flip(image, 1)  # Flip image if needed
    
    # Convert the image from BGR to RGB as required by the TFLite model
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Create a TensorImage object from the RGB image
    input_tensor = vision.TensorImage.create_from_array(rgb_image)
    stop_sign_flag = False
    # Run object detection
    detection_result = detector.detect(input_tensor)
    for detection in detection_result.detections:
        category = detection.categories[0]
        category_name = category.category_name
        if category_name == "stop sign":
            stop_sign_flag = True
            print("Stop Sign Detected")
            # fc.stop()

    if stop_sign_flag:
        fc.stop()
    else:
        fc.forward(20)
        print("Stop Sign Not Detected")

    rawCapture.truncate(0)

    if cv2.waitKey(1) == 27:
        break
