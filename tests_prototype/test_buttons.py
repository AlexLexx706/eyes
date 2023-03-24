import time
import RPi.GPIO as GPIO

TOP_BUTTON = 23
BOTTOM_BUTTON = 22

def main():
    """_summary_
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BOTTOM_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        while 1:
            top_btn_state = GPIO.input(TOP_BUTTON)
            bottom_btn_state = GPIO.input(BOTTOM_BUTTON)
            print(f't:{top_btn_state} b:{bottom_btn_state}')
            time.sleep(0.01)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
