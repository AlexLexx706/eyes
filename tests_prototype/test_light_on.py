import time
from adafruit_servokit import ServoKit
import math

kit = ServoKit(channels=16)
kit._pca.channels[4].duty_cycle = 0xff
kit._pca.channels[5].duty_cycle = 0x6ff
