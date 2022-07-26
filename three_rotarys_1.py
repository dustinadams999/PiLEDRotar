# rotar 1 controls red
import os
import pigpio
from pigpio_encoder import pigpio_encoder

pi = pigpio.pi()

rotary = pigpio_encoder.Rotary(clk=12, dt=20, sw=16)

def main():
  global rotary, pi

  rotary.setup_rotary(min=0,max=255,scale=8,debounce=300,rotary_callback=rotary_callback)
  rotary.setup_switch(debounce=300,short_press=sw_short_callback,sw_short_callback=sw_short_callback,long_press=sw_long_callback,sw_long_callback=sw_long_callback)

  rotary.watch()

def rotary_callback(counter):
  global rotary, pi
  
  os.environ["ROTAR_1_COUNTER"] = '{}'.format(counter)
  print('rotary counter: {}'.format(counter))

def sw_short_callback():
  global rotary

  print('sw short callback')

def sw_long_callback():
  print('sw long callback')

if __name__ == '__main__':
  main()
