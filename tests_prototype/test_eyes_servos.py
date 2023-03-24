import time
from adafruit_servokit import ServoKit
import math

PERIOD = 3
kit = ServoKit(channels=16)

# off
kit._pca.channels[0].duty_cycle = 0
kit._pca.channels[1].duty_cycle = 0


try:
    s_time = time.time()
    while 1:
        v_val = (math.sin((time.time() - s_time) / PERIOD * math.pi * 2.) + 1.) / 2.
        h_val = (math.cos((time.time() - s_time) / PERIOD * math.pi * 2.) + 1.) / 2.
        v_angle = int((180 - 30) * v_val + 30)
        h_angle = int((160 - 60) * h_val + 60)

        kit.servo[0].angle = v_angle
        kit.servo[1].angle = h_angle

        time.sleep(0.01)
except KeyboardInterrupt:
    # off
    kit._pca.channels[0].duty_cycle = 0
    kit._pca.channels[1].duty_cycle = 0
