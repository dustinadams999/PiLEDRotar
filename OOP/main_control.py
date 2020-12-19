import LedFade
import LedRotar
import pigpio
from pigpio_encoder import pigpio_encoder

mode = 0
curr = None
pi = None
main_rotary = None
rgb = (0,0,0)
curr_color = 0
running = True

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

  main_rotary.watch()

def rotary_callback(counter):
  global mode, running, pi, main_rotary, rgb, curr_color, RED_PIN, GREEN_PIN, BLUE_PIN, color_keys, colors
  if mode == 0:
    # fader
    # we can increase or decrease the fading speed here
    print('rotary turn in fader mode')

  else:
    # rotor
    rgb = colors[color_keys[curr_color]](rgb, main_rotary.counter)
      
    pi.set_PWM_dutycycle(RED_PIN, rgb[0])
    pi.set_PWM_dutycycle(GREEN_PIN, rgb[1])
    pi.set_PWM_dutycycle(BLUE_PIN, rgb[2])

def sw_long_callback():
  global mode, pi, running, main_rotary, rgb, curr_color, RED_PIN, GREEN_PIN, BLUE_PIN, color_keys, colors
  print('main_control long press')
  mode = (mode+1)%2
  if mode == 0:
    running = True
    fader()
    # fader
    #curr = LedFade.LedFade(pi)
  else:
    running = False
    # rotor
    #curr = LedRotar.LedRotar(pi, main_rotary)

def sw_short_callback():
  global mode, pi, main_rotary, rgb, curr_color, RED_PIN, GREEN_PIN, BLUE_PIN, color_keys, colors
  print('main_control short press')
  if mode == 0:
    print('click in fader mode')
    # fader
  else:
    curr_color = (curr_color + 1)%3
    main_rotary.counter = rgb[curr_color]

def fader():
  global mode, running, pi, main_rotary, rgb, curr_color, RED_PIN, GREEN_PIN, BLUE_PIN, color_keys, colors
  degrees = 1
  while running:
    time.sleep(.12)

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
