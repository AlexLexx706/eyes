import cv2
import time

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# -----------------------------------------------
# Face Detection using DNN Net
# -----------------------------------------------
# detect faces using a DNN model 
# download model and prototxt from https://github.com/spmallick/learnopencv/tree/master/FaceDetectionComparison/models

# load face detection model
modelFile = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
configFile = "models/deploy.prototxt"
conf_threshold=0.7


net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
p_time = time.time()

while True:
    try:
        _, frame = video_capture.read()

        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False,)

        net.setInput(blob)
        detections = net.forward()
        bboxes = []
 
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                pos = ((x1 + x2) /2, (y1 + y2) / 2)
                print(f'detect:{pos}')
                continue

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        print(f"fps:{fps}")

    except Exception as e:
        print(f'exc: {e}')

video_capture.release()
