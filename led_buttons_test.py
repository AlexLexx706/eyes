# External module imports
import time
import RPi.GPIO as GPIO
import cv2
from pygame import mixer
from adafruit_servokit import ServoKit
import math
from multiprocessing import Process, Queue
import queue
import logging
import curses
import mediapipe as mp



LOG = logging.getLogger(__name__)

# Pin Definitons:
LEFT_LED_PIN = 17
RIGHT_LED_PIN = 27

TOP_BUTTON = 23
BOTTOM_BUTTON = 22

SERVO_EYES_VERTICAL = 0
SERVO_EYES_HORIZONTAL = 1


class Led:
    """_summary_
    """

    def __init__(self, pin, period) -> None:
        self.__pin = pin
        self.__period = period
        self.__start_time = time.time()
        self.__state = 0
        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, GPIO.LOW)

    def update(self, cur_time=time.time()):
        """_summary_

        Args:
            cur_time (_type_, optional): _description_. Defaults to time.time().
        """
        if cur_time >= self.__start_time + self.__period:
            self.__start_time = cur_time - \
                (cur_time - self.__start_time) % self.__period

            if self.__state:
                GPIO.output(self.__pin, GPIO.LOW)
                self.__state = 0
            else:
                GPIO.output(self.__pin, GPIO.HIGH)
                self.__state = 1
class Servo:
    def __init__(self, servos_kit, servo_id, program, period) -> None:
        self.__program = program
        self.__period = period
        self.__id = servo_id

        self.__start_time = time.time()
        self.__prog_index = 0
        self.__servos_kit = servos_kit
        servos_kit.servo[self.__id].angle = program[0]

    def update(self, cur_time=time.time()):
        if cur_time >= self.__start_time + self.__period:
            self.__start_time = cur_time - (cur_time - self.__start_time) % self.__period
            self.__prog_index =  (self.__prog_index + 1) % len(self.__program)
            self.__servos_kit.servo[self.__id].angle = self.__program[self.__prog_index]


class ServoSmooth:
    def __init__(self, servos_kit, servo_id, period, _min, _max) -> None:
        self.__period = period
        self.__id = servo_id
        self.__min = _min
        self.__max = _max
        self.__start_time = time.time()
        self.__servos_kit = servos_kit
        self.__servos_kit.servo[self.__id].angle = self.__min

    def update(self, cur_time=time.time()):
        val = (math.cos((cur_time - self.__start_time) / self.__period * math.pi * 2) + 1) / 2.
        self.__servos_kit.servo[self.__id].angle = int((self.__max - self.__min) * val + self.__min)


def camera_and_sound(exit_queue, pos_queue):
    faceCascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_frontalface_alt.xml')
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

    GPIO.setmode(GPIO.BCM)

    left_led_pin = Led(LEFT_LED_PIN, 0.1)
    right_led_pin = Led(RIGHT_LED_PIN, 0.1)
    GPIO.setup(TOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BOTTOM_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    v_eyes_servo = ServoSmooth(servos_kit, SERVO_EYES_VERTICAL, 10, 30, 180)
    h_eyes_servo = ServoSmooth(servos_kit, SERVO_EYES_HORIZONTAL, 10, 40, 160)

    print("Here we go! Press CTRL+C to exit")
    exit_queue = Queue()
    pos_queue = Queue(3)
    camera_and_sound_proc = Process(target=camera_and_sound, args=(exit_queue, pos_queue))
    camera_and_sound_proc.start()

    cur_pos = (640/2, 480/2)
    
    # inittialization curses 
    # screen = curses.initscr()
    # curses.noecho()
    # curses.cbreak()
    # screen.keypad(True)
    # screen.nodelay(True)
    # screen.leaveok(True)
    # screen.erase()
    
    vertical_angle = 100
    hirizontal_angle = 100

    try:
        while 1:
            # char = screen.getch()
            # if char == curses.KEY_RIGHT:
            #     vertical_angle += 1
            #     vertical_angle = vertical_angle if vertical_angle <= 180 else 180
            # elif char == curses.KEY_LEFT:
            #     vertical_angle -= 1
            #     vertical_angle = vertical_angle if vertical_angle >= 0 else 0
            # elif char == curses.KEY_UP:
            #     hirizontal_angle += 1
            #     hirizontal_angle = hirizontal_angle if hirizontal_angle <= 180 else 180
            # elif char == curses.KEY_DOWN:
            #     hirizontal_angle -= 1
            #     hirizontal_angle = hirizontal_angle if hirizontal_angle >= 0 else 0

            cur_time = time.time()
            left_led_pin.update(cur_time)
            right_led_pin.update(cur_time)

            # v_eyes_servo.update(cur_time)
            # h_eyes_servo.update(cur_time)

            top_btn_state = GPIO.input(TOP_BUTTON)
            bottom_btn_state = GPIO.input(BOTTOM_BUTTON)

            # move up 
            if bottom_btn_state:
                servos_kit.continuous_servo[15].throttle = 0.3 # up
            # move down
            elif top_btn_state:
                servos_kit.continuous_servo[15].throttle = -0.1 # down

            # print(f't:{top_btn_state} b:{bottom_btn_state}')
            try:
                pos = pos_queue.get_nowait()
                cur_pos = pos
            except queue.Empty:
                pass
            k_x = (640 - cur_pos[0]) / 640
            k_y = (cur_pos[1]) / 480
            v_angle = int((180 - 30) * k_x + 30)
            h_angle = int((160 - 60) * k_y + 60)
            servos_kit.servo[0].angle = v_angle
            servos_kit.servo[1].angle = h_angle

            # print(f"v_angle:{v_angle:3}, h_angle:{h_angle:3}")
            #print(f'x:{cur_pos[0]:4} y:{cur_pos[1]:4}')
            # screen.addstr(0, 1, f'v:{vertical_angle:4} h:{hirizontal_angle:4}')

            time.sleep(0.01)
    except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
        # pwm.stop() # stop PWM
        GPIO.cleanup()  # cleanup all GPIO
        exit_queue.put(1)
        camera_and_sound_proc.join()

if __name__ == "__main__":
    main()
