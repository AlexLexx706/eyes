import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

servos_kit = ServoKit(channels=16)

TOP_BUTTON = 23
BOTTOM_BUTTON = 22

def main():
    """_summary_
    """

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BOTTOM_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    servos_kit.continuous_servo[2].throttle = 0.3  

    try:
        while 1:
            top_btn_state = GPIO.input(TOP_BUTTON)
            bottom_btn_state = GPIO.input(BOTTOM_BUTTON)
            
            # move up 
            if bottom_btn_state:
                servos_kit.continuous_servo[2].throttle = 0.3
            # move down
            elif top_btn_state:
                servos_kit.continuous_servo[2].throttle = -0.1
            print(f't:{top_btn_state} b:{bottom_btn_state}')

            time.sleep(0.01)
    except KeyboardInterrupt:
        servos_kit.continuous_servo[2].throttle = 0
        GPIO.cleanup()


if __name__ == "__main__":
    main()
