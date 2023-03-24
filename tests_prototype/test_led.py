import time
from adafruit_servokit import ServoKit
import math

PERIOD = 0.5
kit = ServoKit(channels=16)
kit._pca.channels[4].duty_cycle = 0
kit._pca.channels[5].duty_cycle = 0


try:
    s_time = time.time()
    while 1:
        val = (math.sin((time.time() - s_time) / PERIOD * math.pi * 2.) + 1.) / 2.
        val2 = (math.cos((time.time() - s_time) / PERIOD * math.pi * 2.) + 1.) / 2.
        kit._pca.channels[4].duty_cycle = int(val * 0xffff)
        kit._pca.channels[5].duty_cycle = int(val2 * 0xffff)
        time.sleep(0.01)
except KeyboardInterrupt:
    kit._pca.channels[4].duty_cycle = 0
    kit._pca.channels[5].duty_cycle = 0
