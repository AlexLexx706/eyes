import numpy as np
import cv2
import time

faceCascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

p_time = time.time()

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=1,
        minSize=(100,100)
    )

    for (x,y,w,h) in faces:
        res = (x + w /2, y + h / 2)
        print(f'detect:{res}')

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    print(f'fps:{fps}')

cap.release()
# cv2.destroyAllWindows()
