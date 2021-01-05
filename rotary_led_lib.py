import pigpio
from pigpio_encoder import pigpio_encoder

RED_PIN=5
GREEN_PIN=6
BLUE_PIN=26

pi = pigpio.pi()
prev_counter = 0

def main():
  global my_rotary, curr_color, rgb, pi

  my_rotary = pigpio_encoder.Rotary(clk=18, dt=17, sw=27)
  my_rotary.setup_rotary(min=0,max=255,scale=8,debounce=50,rotary_callback=rotary_callback)
  my_rotary.setup_switch(debounce=300,sw_short_callback=sw_short_callback)
  my_rotary.setup_switch(debounce=100,long_press=sw_long_callback,sw_long_callback=sw_long_callback)
  my_rotary.watch()

def rotary_callback(counter):
  # TODO: update for new library usage (look at main_control.py)
  global rgb, my_rotary, curr_color, pi, offset, prev_counter

  if not my_rotary.fader_mode:
    # rotary mode
    rgb = colors[color_keys[curr_color]](rgb, my_rotary.counter)
    
    pi.set_PWM_dutycycle(RED_PIN, rgb[0])
    pi.set_PWM_dutycycle(GREEN_PIN, rgb[1])
    pi.set_PWM_dutycycle(BLUE_PIN, rgb[2])

    print('rgb: {}'.format(rgb))

  else:
    # fader mode
    if (counter - prev_counter) < 0:
      # going down/left
      # increasing my_rotary.fader_scale will decrease speed
      my_rotary.fader_scale = bound(50, 500, my_rotary.fader_scale+5)
    else:
      my_rotary.fader_scale = bound(50, 500, my_rotary.fader_scale-5)

  prev_counter = counter

def sw_short_callback():
  # TODO: update for new library usage (look at main_control.py)
  global my_rotary, rgb, curr_color, offset

  print('click')

  if my_rotary.fader_mode:
    curr_color = (curr_color + 1)%3
    my_rotary.counter = rgb[curr_color]

    print('rgb: {}, counter: {}'.format(rgb, my_rotary.counter))
    print('currently color: {}'.format(color_keys[curr_color]))

def sw_long_callback():
  global my_rotary
  # TODO: update for new library usage (look at main_control.py)
  my_rotary.fader_mode = (not my_rotary.fader_mode)

  print('sw long callback')

def bound(low, high, value):
  return max(low, min(high, value))

if __name__ == '__main__':
  main()
