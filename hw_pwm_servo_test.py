import time
from rpi_hardware_pwm import HardwarePWM

p = HardwarePWM(pwm_channel=0, hz=50)
p.start(2.5) # full duty cycle

try:
  while True:
    p.change_duty_cycle(5)
    time.sleep(1.0)
    p.change_duty_cycle(7.5)
    time.sleep(1.0)
    p.change_duty_cycle(10)
    time.sleep(1.0)
    p.change_duty_cycle(12.5)
    time.sleep(1.0)
    p.change_duty_cycle(10)
    time.sleep(1.0)
    p.change_duty_cycle(7.5)
    time.sleep(1.0)
    p.change_duty_cycle(5)
    time.sleep(1.0)
    p.change_duty_cycle(2.5)
    time.sleep(1.0)
except KeyboardInterrupt:
  p.stop()
