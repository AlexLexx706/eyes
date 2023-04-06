import numpy as np
import cv2
import time
import face_recognition

faceCascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

p_time = time.time()

while True:
    ret, img = cap.read()
    faces = face_recognition.face_locations(img)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # faces = faceCascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.2,
    #     minNeighbors=1,
    #     minSize=(100,100))
    for top, right, bottom, left in faces:
        x = left
        y = top
        print(x,y)
        cv2.rectangle(img,(left, top),(right, bottom),(255,0,0),2)

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow('video',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
    	break
cap.release()
# cv2.destroyAllWindows()
