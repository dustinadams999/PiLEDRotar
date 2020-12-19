import LedFade
import LedRotar
import math
import pigpio
import time
from pigpio_encoder import pigpio_encoder

mode = 0
curr = None
pi = None
main_rotary = None
rgb = (0,0,0)
curr_color = 0
running = True

curr_counter = 0

speed_factor=30

RED_PIN=5
GREEN_PIN=6
BLUE_PIN=26

color_keys = ['R', 'G', 'B']
colors = {
  'R': (lambda rgb,counter: ((max(0, min(255, counter)), rgb[1], rgb[2]))),
  'G': (lambda rgb,counter: ((rgb[0], max(0, min(255, counter)), rgb[2]))),
  'B': (lambda rgb,counter: ((rgb[0], rgb[1], max(0, min(255, counter)))))
}

def main():
  global mode, pi, main_rotary, rgb, curr_color, RED_PIN, GREEN_PIN, BLUE_PIN, color_keys, colors

  main_rotary = pigpio_encoder.Rotary(clk=18, dt=17, sw=27)
  main_rotary.setup_rotary(min=0,max=255,scale=8,debounce=50,rotary_callback=rotary_callback)
  main_rotary.setup_switch(debounce=300,sw_short_callback=sw_short_callback)
  main_rotary.setup_switch(debounce=100,long_press=sw_long_callback,sw_long_callback=sw_long_callback)
  
  pi = pigpio.pi()
  
  fader()

  main_rotary.watch()

def rotary_callback(counter):
  global mode, curr_counter, speed_factor, running, pi, main_rotary, rgb, curr_color, RED_PIN, GREEN_PIN, BLUE_PIN, color_keys, colors
  if mode == 0:
    # fader
    # we can increase or decrease the fading speed here
    if abs(counter - curr_counter)//8 == 1:
      speed_factor += (counter - curr_counter)//8
    if counter == curr_counter or speed_factor < 0 or counter <= 0:
      mode = (mode+1)%2
      running = False
    print('rotary turn in fader mode. speed_factor: {}, curr_counter: {}, counter: {}, running: {}'.format(speed_factor, curr_counter, counter, running))

  else:
    # rotor
    rgb = colors[color_keys[curr_color]](rgb, main_rotary.counter)
      
    pi.set_PWM_dutycycle(RED_PIN, rgb[0])
    pi.set_PWM_dutycycle(GREEN_PIN, rgb[1])
    pi.set_PWM_dutycycle(BLUE_PIN, rgb[2])

  curr_counter = counter

def sw_long_callback():
  global mode, pi, running, main_rotary, rgb, curr_color, RED_PIN, GREEN_PIN, BLUE_PIN, color_keys, colors
  print('main_control long press. current mode: {}, next mode: {}'.format(mode, (mode+1)%2))
  mode = (mode+1)%2
  if mode == 0:
    # fader
    running = True
    fader()
  else:
    # rotor
    running = False

def sw_short_callback():
  global mode, pi, main_rotary, rgb, curr_color, RED_PIN, GREEN_PIN, BLUE_PIN, color_keys, colors
  print('main_control short press')
  if mode == 0:
    # fader
    print('click in fader mode')
  else:
    curr_color = (curr_color + 1)%3
    main_rotary.counter = rgb[curr_color]

def fader():
  global mode, speed_factor, running, pi, main_rotary, rgb, curr_color, RED_PIN, GREEN_PIN, BLUE_PIN, color_keys, colors
  degrees = 1
  mode = 0
  r = 255
  g = 0
  b = 0
  while running:
    time.sleep(speed_factor/250)

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

  rgb = (r,g,b)

if __name__ == '__main__':
  main()
