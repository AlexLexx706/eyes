import time
from adafruit_servokit import ServoKit
import math

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

# start_time = time.time()
# freq = 25.
# period = 3.
# while 1:
#     cur_time = time.time()
#     value = int((math.cos((cur_time - start_time) / period * math.pi * 2) + 1.) / 2. * 180.)
#     kit.servo[15].angle = value
#     time.sleep(1. / freq)
#     # print(value)

kit.servo[0].angle = 180
kit.continuous_servo[15].throttle = -1
time.sleep(1)
kit.continuous_servo[15].throttle = 1
time.sleep(1)
kit.servo[0].angle = 0
kit.continuous_servo[15].throttle = 0