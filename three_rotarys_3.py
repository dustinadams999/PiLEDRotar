# rotar 3 controls blue
import pigpio
import os
from pigpio_encoder import pigpio_encoder

rotary = pigpio_encoder.Rotary(clk=11, dt=10, sw=9)
pi = pigpio.pi()
BLUE_PIN=26

def main():
  rotary.setup_rotary(min=0,max=255,scale=8,debounce=300,rotary_callback=rotary_callback)
  rotary.setup_switch(debounce=300,short_press=sw_short_callback,sw_short_callback=sw_short_callback,long_press=sw_long_callback,sw_long_callback=sw_long_callback)

  rotary.watch()

def rotary_callback(counter):
  print('blue: {}'.format(counter))
  pi.set_PWM_dutycycle(BLUE_PIN, min(counter, 255))

def sw_short_callback():
  print('sw short callback')

def sw_long_callback():
  print('sw long callback')

if __name__ == '__main__':
  main()
