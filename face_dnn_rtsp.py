import cv2
import time
import os

RTSP_URL = 'rtsp://192.168.1.4:8554/unicast'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

video_capture = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
time.sleep(2)

# -----------------------------------------------
# Face Detection using DNN Net
# -----------------------------------------------
# detect faces using a DNN model 
# download model and prototxt from https://github.com/spmallick/learnopencv/tree/master/FaceDetectionComparison/models

def detectFaceOpenCVDnn(net, frame, conf_threshold=0.7):
    
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
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8,)
            print((x1, y1))
            top=x1
            right=y1
            bottom=x2-x1
            left=y2-y1

            #  blurry rectangle to the detected face
            # face = frame[right:right+left, top:top+bottom]
            # face = cv2.GaussianBlur(face,(23, 23), 30)
            # frame[right:right+face.shape[0], top:top+face.shape[1]] = face

    return frame, bboxes

# load face detection model
modelFile = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
configFile = "models/deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

detectionEnabled = True
p_time = time.time()

while True:
    try:
        _, frameOrig = video_capture.read()
        frame = cv2.resize(frameOrig, (640, 480))
        #frame = cv2.resize(frameOrig, (320, 240))

        if(detectionEnabled == True):
            outOpencvDnn, bboxes = detectFaceOpenCVDnn(net, frame)


        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        cv2.imshow('@ElBruno - Face Blur usuing DNN', frame)

    except Exception as e:
        print(f'exc: {e}')
        pass

    # key controller
    key = cv2.waitKey(1) & 0xFF
    if key == ord("d"):
        detectionEnabled = not detectionEnabled

    if key == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
