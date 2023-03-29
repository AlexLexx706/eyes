import time
import RPi.GPIO as GPIO
import simpleaudio as sa
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
    wave_obj = sa.WaveObject.from_wave_file("../back.wav")

    servos_kit.servo[1].angle = 110
    servos_kit.servo[0].angle = 105
    servos_kit._pca.channels[4].duty_cycle = 0
    servos_kit._pca.channels[5].duty_cycle = 0

    servos_kit.continuous_servo[2].throttle = 0.3
    top_btn_state = 0
    while not top_btn_state:
        top_btn_state = GPIO.input(TOP_BUTTON)
        time.sleep(0.01)
    servos_kit.continuous_servo[2].throttle = 0

    time.sleep(2)
    servos_kit._pca.channels[5].duty_cycle = 0xffff
    time.sleep(3)
    play_obj = wave_obj.play()
    time.sleep(2.5)
    try:
        servos_kit.continuous_servo[2].throttle = -0.02
        for i in range(60):
            servos_kit.continuous_servo[2].throttle = -0.08
            servos_kit.servo[1].angle = 110 - i*0.83
            time.sleep(0.08)
            servos_kit.continuous_servo[2].throttle = 0
            time.sleep(0.08)

        servos_kit.continuous_servo[2].throttle = -0.3
        bottom_btn_state = 0
        while not bottom_btn_state:
            bottom_btn_state = GPIO.input(BOTTOM_BUTTON)
        servos_kit.continuous_servo[2].throttle = 0
        servos_kit._pca.channels[5].duty_cycle = 0
        play_obj.stop()
    except KeyboardInterrupt:
        servos_kit._pca.channels[5].duty_cycle = 0
        play_obj.stop()
        servos_kit.continuous_servo[2].throttle = 0
        GPIO.cleanup()

if __name__ == "__main__":
    main()

