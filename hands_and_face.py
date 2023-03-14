import cv2
import time
import mediapipe as mp

video_capture = cv2.VideoCapture(0)
time.sleep(2)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

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
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if(detectionEnabled == True):
            outOpencvDnn, bboxes = detectFaceOpenCVDnn(net, frame)


        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        results = hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                x = 0.
                y = 0.
                for lm in handLms.landmark:
                    x += lm.x
                    y += lm.y
                h, w, c = frame.shape
                x = int(x / len(handLms.landmark) * w)
                y = int(y / len(handLms.landmark) * h)
                cv2.circle(frame, (x,y), 10, (255, 0, 0), cv2.FILLED)
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