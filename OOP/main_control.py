import LedFade
import LedRotar
import pigpio
from pigpio_encoder import pigpio_encoder

mode = 0

curr = None
pi = None
led_fader = None
led_rotar = None
main_rotary = None

def main():
  global curr, pi, led_fader, led_rotar

  main_rotary = pigpio_encoder.Rotary(clk=18, dt=17, sw=27)
  main_rotary.setup_switch(debounce=300,sw_short_callback=sw_short_callback)
  main_rotary.setup_switch(debounce=100,long_press=sw_long_callback,sw_long_callback=sw_long_callback)
  
  pi = pigpio.pi()
  #led_fader = LedFade(pi)
  #led_rotar = LedRotar(pi, main_rotary)

  curr = LedFade.LedFade(pi)

  main_rotary.watch()

def sw_long_callback():
  global mode, curr
  print('main_control long press')
  mode = (mode+1)%2
  if mode == 0:
    curr = LedFade.LedFade(pi)
  else:
    curr = LedRotar.LedRotar(pi, main_rotary)

def sw_short_callback():
  print('main_control short press')

if __name__ == '__main__':
  main()
