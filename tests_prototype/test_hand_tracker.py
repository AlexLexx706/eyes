# External module imports
import time
import cv2
from pygame import mixer
from adafruit_servokit import ServoKit
import math
from multiprocessing import Process, Queue
import queue
import mediapipe as mp

SERVO_EYES_VERTICAL = 0
SERVO_EYES_HORIZONTAL = 1


def hand_detection(exit_queue, pos_queue):
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                        max_num_hands=2,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)

    while 1:
        try:
            exit_queue.get(block=False)
            return
        except queue.Empty:
            pass

        ret, frame = cap.read()
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks[:1]:
                x = 0.
                y = 0.
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x *w), int(lm.y*h)
                    x += lm.x
                    y += lm.y
                h, w, c = frame.shape
                x = int(x / len(handLms.landmark) * w)
                y = int(y / len(handLms.landmark) * h)
                pos_queue.put_nowait((x, y))


def main():
    """_summary_
    """
    servos_kit = ServoKit(channels=16)
    exit_queue = Queue()
    pos_queue = Queue(3)
    camera_and_sound_proc = Process(target=hand_detection, args=(exit_queue, pos_queue))
    camera_and_sound_proc.start()

    cur_pos = (640 / 2., 480 / 2.)
    vertical_angle = 100
    hirizontal_angle = 100

    try:
        while 1:
            cur_time = time.time()
            try:
                cur_pos = pos_queue.get_nowait()
            except queue.Empty:
                pass

            k_x = (640 - cur_pos[0]) / 640
            k_y = (cur_pos[1]) / 480
            v_angle = int((180 - 30) * k_x + 30)
            h_angle = int((160 - 60) * k_y + 60)
            servos_kit.servo[SERVO_EYES_VERTICAL].angle = v_angle
            servos_kit.servo[SERVO_EYES_HORIZONTAL].angle = h_angle
            time.sleep(0.01)
    except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
        servos_kit._pca.channels[0].duty_cycle = 0
        servos_kit._pca.channels[0].duty_cycle = 0

        exit_queue.put(1)
        camera_and_sound_proc.join()

if __name__ == "__main__":
    main()
