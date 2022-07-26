import os
import pigpio


RED_PIN=5
GREEN_PIN=6
BLUE_PIN=26

pi = pigpio.pi()

while(True):
  pi.set_PWM_dutycycle(RED_PIN, int(os.environ["ROTAR_1_COUNTER"]))
  pi.set_PWM_dutycycle(GREEN_PIN, int(os.environ["ROTAR_2_COUNTER"]))
  pi.set_PWM_dutycycle(BLUE_PIN, int(os.environ["ROTAR_3_COUNTER"]))
