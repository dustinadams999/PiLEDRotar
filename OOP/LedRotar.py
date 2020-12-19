RED_PIN=5
GREEN_PIN=6
BLUE_PIN=26

rgb = (0,0,0)
curr_color = 0
mode = 0

pi = None
my_rotary = None

color_keys = ['R', 'G', 'B']

colors = {
  'R': (lambda rgb,counter: ((bound(0, 255, counter), rgb[1], rgb[2]))),
  'G': (lambda rgb,counter: ((rgb[0], bound(0, 255, counter), rgb[2]))),
  'B': (lambda rgb,counter: ((rgb[0], rgb[1], bound(0, 255, counter))))
}
class LedRotar():
  def __init__(self, p, my_r):
    pi = p
    my_rotary = my_r

    rgb = colors[color_keys[curr_color]](rgb, my_rotary.counter)

    print('starting on color: {}, counter: {}'.format(color_keys[curr_color], my_rotary.counter ))

    my_rotary.setup_rotary(min=0,max=255,scale=8,debounce=50,rotary_callback=rotary_callback)
    my_rotary.setup_switch(debounce=300,sw_short_callback=sw_short_callback)
    my_rotary.setup_switch(debounce=100,long_press=sw_long_callback,sw_long_callback=sw_long_callback)

    pi.set_PWM_dutycycle(RED_PIN, rgb[0])
    pi.set_PWM_dutycycle(GREEN_PIN, rgb[1])
    pi.set_PWM_dutycycle(BLUE_PIN, rgb[2])

    my_rotary.watch()

  def rotary_callback(counter):
    #global rgb, my_rotary, curr_color, pi, offset
    
    rgb = colors[color_keys[curr_color]](rgb, my_rotary.counter)
    
    pi.set_PWM_dutycycle(RED_PIN, rgb[0])
    pi.set_PWM_dutycycle(GREEN_PIN, rgb[1])
    pi.set_PWM_dutycycle(BLUE_PIN, rgb[2])

    print('rgb: {}'.format(rgb))

  def sw_short_callback():
    #global my_rotary, rgb, curr_color, offset

    print('click')
    curr_color = (curr_color + 1)%3
    my_rotary.counter = rgb[curr_color]

    print('rgb: {}, counter: {}'.format(rgb, my_rotary.counter))
    print('currently color: {}'.format(color_keys[curr_color]))

  def sw_long_callback():
    print('sw long callback in LedRotar')

  def bound(low, high, value):
    return max(low, min(high, value))



