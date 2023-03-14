# External module imports
import time
import RPi.GPIO as GPIO
import cv2
from pygame import mixer

#Instantiate mixer
mixer.init()
#Load audio file
mixer.music.load('output.wav')
#Set preferred volume
mixer.music.set_volume(0.2)



faceCascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

# Pin Definitons:
LEFT_LED_PIN = 17
RIGHT_LED_PIN = 27

TOP_BUTTON = 23
BOTTOM_BUTTON = 22

SERVO_EYES_VERTICAL = 12
SERVO_EYES_HORIZONTAL = 13


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
    def __init__(self, pin, program, period) -> None:
        self.__program = program
        self.__period = period
        #hw chanel 0
        print(f'pin:{pin} program:{program}')
        # PWM pin set as output
        GPIO.setup(pin, GPIO.OUT)
        self.__pwm = GPIO.PWM(pin, 50)
        self.__change_duty_cycle = self.__pwm.ChangeDutyCycle

        self.__start_time = time.time()
        self.__prog_index = 0
        self.__pwm.start(program[0])

    def update(self, cur_time=time.time()):
        if cur_time >= self.__start_time + self.__period:
            self.__start_time = cur_time - (cur_time - self.__start_time) % self.__period
            self.__prog_index =  (self.__prog_index + 1) % len(self.__program)
            self.__change_duty_cycle(self.__program[self.__prog_index])

def main():
    """_summary_
    """

    GPIO.setmode(GPIO.BCM)

    left_led_pin = Led(LEFT_LED_PIN, 0.1)
    right_led_pin = Led(RIGHT_LED_PIN, 0.1)
    GPIO.setup(TOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BOTTOM_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    v_eyes_servo = Servo(SERVO_EYES_VERTICAL, [5, 7.5, 10, 12.5, 10, 7.5, 5, 2.5], 2)
    h_eyes_servo = Servo(SERVO_EYES_HORIZONTAL, [5, 7.5, 9, 7.5], 2)

    print("Here we go! Press CTRL+C to exit")
    play = 0

    try:
        while 1:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=1,
                minSize=(100,100)
            )
            for (x,y,w,h) in faces:
                print(x,y)
                if not mixer.music.get_busy():
                    mixer.music.play()
                    
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]

            cur_time = time.time()
            left_led_pin.update(cur_time)
            right_led_pin.update(cur_time)
            v_eyes_servo.update(cur_time)
            h_eyes_servo.update(cur_time)
            print(f'top_btn:{GPIO.input(TOP_BUTTON)} '
                  f'bottom_btn:{GPIO.input(BOTTOM_BUTTON)}')
            time.sleep(0.1)
    except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
        # pwm.stop() # stop PWM
        GPIO.cleanup()  # cleanup all GPIO


if __name__ == "__main__":
    main()
