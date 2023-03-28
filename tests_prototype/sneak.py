import time
import RPi.GPIO as GPIO
import simpleaudio as sa
from adafruit_servokit import ServoKit
import os
servos_kit = ServoKit(channels=16)

TOP_BUTTON = 23
BOTTOM_BUTTON = 22
PIR = 24 #Assign pin 8 to PIR

sound_1_path = os.path.join(os.path.split(__file__)[0], '../sneak.wav')

def main():
    """_summary_
    """

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BOTTOM_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIR, GPIO.IN) #Setup GPIO pin PIR as input
    time.sleep(2) #Give sensor time to startup

    wave_obj = sa.WaveObject.from_wave_file(sound_1_path)

    while 1:
        while True:
            if GPIO.input(PIR):
                break
            time.sleep(0.1)

        servos_kit._pca.channels[4].duty_cycle = 0xff
        servos_kit._pca.channels[5].duty_cycle = 0x6ff
        servos_kit.continuous_servo[2].throttle = -0.1
        servos_kit.servo[0].angle = 105
        bottom_btn_state = 0
        while not bottom_btn_state:
            top_btn_state = GPIO.input(TOP_BUTTON)
            bottom_btn_state = GPIO.input(BOTTOM_BUTTON)
            time.sleep(0.01)
        servos_kit.continuous_servo[2].throttle = 0
        time.sleep(1)

        servos_kit.continuous_servo[2].throttle = 0.22
        time.sleep(1.3)
        servos_kit.continuous_servo[2].throttle = 0

        play_obj = wave_obj.play()
        time.sleep(1)
        servos_kit._pca.channels[4].duty_cycle = 0x0
        servos_kit._pca.channels[5].duty_cycle = 0x0
        time.sleep(0.12)
        servos_kit._pca.channels[4].duty_cycle = 0xff
        servos_kit._pca.channels[5].duty_cycle = 0x6ff
        time.sleep(1.6)

        # time.sleep(2.8)
        servos_kit.servo[1].angle = 90
        servos_kit.servo[0].angle = 30
        time.sleep(2)
        servos_kit.servo[0].angle = 180
        time.sleep(2)
        servos_kit.servo[0].angle = 30
        time.sleep(2)
        servos_kit.servo[0].angle = 105
        time.sleep(0.9)
        servos_kit._pca.channels[4].duty_cycle = 0x0
        servos_kit._pca.channels[5].duty_cycle = 0x0
        time.sleep(0.08)
        servos_kit._pca.channels[4].duty_cycle = 0xff
        servos_kit._pca.channels[5].duty_cycle = 0x6ff
        time.sleep(1)
        # time.sleep(2)

        servos_kit.continuous_servo[2].throttle = -0.3
        bottom_btn_state = 0
        while not bottom_btn_state:
            top_btn_state = GPIO.input(TOP_BUTTON)
            bottom_btn_state = GPIO.input(BOTTOM_BUTTON)
        servos_kit.continuous_servo[2].throttle = 0
        play_obj.stop()
        
        #eyes off
        servos_kit._pca.channels[4].duty_cycle = 0x0
        servos_kit._pca.channels[5].duty_cycle = 0x0

        #all servo off
        servos_kit._pca.channels[0].duty_cycle = 0
        servos_kit._pca.channels[1].duty_cycle = 0
        servos_kit._pca.channels[2].duty_cycle = 0

        #     # move up
        #     if bottom_btn_state:
        #         servos_kit.continuous_servo[2].throttle = 0.3
        #     # move down
        #     elif top_btn_state:
        #         servos_kit.continuous_servo[2].throttle = -0.1
        #     print(f't:{top_btn_state} b:{bottom_btn_state}')
        #
        #     time.sleep(0.01)
        #
        # except KeyboardInterrupt:
        #     servos_kit.continuous_servo[2].throttle = 0
        #     GPIO.cleanup()


if __name__ == "__main__":
    main()

