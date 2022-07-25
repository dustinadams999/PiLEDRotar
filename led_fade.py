import math
import pigpio
from pigpio_encoder import pigpio_encoder
import time

def main():
  RED_PIN=5
  GREEN_PIN=6
  BLUE_PIN=26

  FACTOR=100

  pi = pigpio.pi()

  r = 0
  g = 255
  b = 0

  r_factor = 1
  g_factor = 3
  b_factor = 1

  mode = 0
  degrees = 1

  while 1:
    #time.sleep(.12)
    time.sleep(.05)

    # at the beginning r = 255, g = 0, b = 0 (b is still, g is fast moving)
    if mode == 0:
      r = round((255/2)*(1+math.cos(math.radians(degrees))))
      g = round((255/2)*(1-math.cos(math.radians(3*degrees))))
      if degrees%180 == 0:
        mode = (mode+1)%3
    # at the end r = 0, g = 255, b = 0


    # at the beginning r = 0, g = 255, b = 0 (r is still, b is fast moving)
    elif mode == 1:
      b = round((255/2)*(1+math.cos(math.radians(degrees))))
      g = round((255/2)*(1-math.cos(math.radians(3*degrees))))
      if degrees%180 == 0:
        mode = (mode+1)%3
    # at the end r = 0, g = 0, b = 255

    # at the beginning r = 0, g = 0, b = 255 (g is still, r is fast moving)
    elif mode == 2:
      b = round((255/2)*(1+math.cos(math.radians(degrees))))
      r = round((255/2)*(1-math.cos(math.radians(3*degrees))))
      if degrees%180 == 0:
        degrees = 1
        mode = (mode+1)%3
    # at the end r = 255, g = 0, b = 0

    pi.set_PWM_dutycycle(RED_PIN, r)
    pi.set_PWM_dutycycle(GREEN_PIN, g)
    pi.set_PWM_dutycycle(BLUE_PIN, b)


    degrees = (degrees + 1)%360

if __name__ == '__main__':
  main()
