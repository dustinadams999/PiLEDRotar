import LedFade
import LedRotar
import pigpio
from pigpio_encoder import pigpio_encoder

def main():



  my_rotary = pigpio_encoder.Rotary(clk=18, dt=17, sw=27)
  my_rotary.setup_switch(debounce=100,long_press=sw_long_callback,sw_long_callback=sw_long_callback)
  
  pi = pigpio.pi()
  led_fader = LedFade(pi)
  led_rotar = LedRotar(pi, my_rotary)


  my_rotary.watch()

def sw_long_callback():
  print('main_control long press')

if __name__ == '__main__':
  main()