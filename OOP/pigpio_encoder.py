# Rotary encoder class based on pigpio library
# version: 0.2.2

import pigpio
import time


class Rotary:

	# Set the sequence for CW and CCW
	sequence = []
	sequence_up = ['dt1', 'clk1', 'dt0', 'clk0']
	sequence_down = ['clk1', 'dt1', 'clk0', 'dt0']

	# Default values for the rotary encoder
	min = 0
	max = 100
	scale = 1
	debounce = 300
	counter = 0
	last_counter = 0
	rotary_callback = None

	# Default values for the switch
	sw_debounce = 300
	long_press_opt = False
	sw_short_callback = None
	sw_long_callback = None
	wait_time = time.time()
	long = False

	def __init__(self, clk=None, dt=None, sw=None):
		print('WARNING: using altered pigpio_encoder library.')
		if not clk or not dt:
			raise BaseException("CLK and DT pin must be specified!")
		self.clk = clk
		self.dt = dt
		self.clk_input = pigpio.pi()
		self.dt_input = pigpio.pi()
		self.clk_input.set_glitch_filter(self.clk, self.debounce)
		self.dt_input.set_glitch_filter(self.dt, self.debounce)

		# piLED variables
		self.fader_mode = True # fader or rotar
		self.fader_phase = 0
		self.fader_scale = 100
		self.degrees = 1
		self.r = 255
		self.g = 0
		self.b = 0

		if sw is not None:
			self.sw = sw
			self.sw_input = pigpio.pi()
			self.sw_input.set_pull_up_down(self.sw, pigpio.PUD_UP)
			self.sw_input.set_glitch_filter(self.sw, self.sw_debounce)

		def clk_fall(gpio, level, tick):
			if len(self.sequence) > 2:
				self.sequence.clear()
			self.sequence.append('clk1')

		def clk_rise(gpio, level, tick):
			self.sequence.append('clk0')
			if self.sequence == self.sequence_up:
				if self.counter > self.min:
					self.counter -= self.scale
				# comment out the top two lines and uncomment out the bottom two lines to reverse the rotar
				#if self.counter < self.max:
				#	self.counter += self.scale
				self.sequence.clear()

		def dt_fall(gpio, level, tick):
			if len(self.sequence) > 2:
				self.sequence.clear()
			self.sequence.append('dt1')

		def dt_rise(gpio, level, tick):
			self.sequence.append('dt0')
			if self.sequence == self.sequence_down:
				if self.counter < self.max:
					self.counter += self.scale
				# comment out the top two lines and uncomment out the bottom two lines to reverse the rotar
				#if self.counter > self.min:
				#	self.counter -= self.scale
				self.sequence.clear()

		def sw_rise(gpio, level, tick):
			if self.long_press_opt:
				if not self.long:
					self.short_press()

		def sw_fall(gpio, level, tick):
			if self.long_press_opt:
				self.long = False
				press_time = time.time()
				while self.sw_input.read(self.sw) == 0:
					self.wait_time = time.time()
					time.sleep(0.1)
					if self.wait_time - press_time > 1.5:
						self.long_press()
						self.long = True
						break
			else:
				self.short_press()


		self.clk_falling = self.clk_input.callback(self.clk, pigpio.FALLING_EDGE, clk_fall)
		self.clk_rising = self.clk_input.callback(self.clk, pigpio.RISING_EDGE, clk_rise)
		self.dt_falling = self.dt_input.callback(self.dt, pigpio.FALLING_EDGE, dt_fall)
		self.dt_rising = self.dt_input.callback(self.dt, pigpio.RISING_EDGE, dt_rise)
		self.sw_falling = self.sw_input.callback(self.sw, pigpio.FALLING_EDGE, sw_fall)
		self.sw_rising = self.sw_input.callback(self.sw, pigpio.RISING_EDGE, sw_rise)


	def setup_rotary(self, **kwargs):
		if 'min' in kwargs:
			self.min = kwargs['min']
			self.counter = self.min
			self.last_counter = self.min
		if 'max' in kwargs:
			self.max = kwargs['max']
		if 'scale' in kwargs:
			self.scale = kwargs['scale']
		if 'debounce' in kwargs:
			self.debounce = kwargs['debounce']
			self.clk_input.set_glitch_filter(self.clk, self.debounce)
			self.dt_input.set_glitch_filter(self.dt, self.debounce)
		if 'rotary_callback' in kwargs:
			self.rotary_callback = kwargs['rotary_callback']

	def setup_switch(self, **kwargs):
		if 'debounce' in kwargs:
			self.sw_debounce = kwargs['debounce']
		if 'long_press' in kwargs:
			self.long_press_opt = kwargs['long_press']
		if 'sw_short_callback' in kwargs:
			self.sw_short_callback = kwargs['sw_short_callback']
		if 'sw_long_callback' in kwargs:
			self.sw_long_callback = kwargs['sw_long_callback']

	def watch(self):
		# self.callback = callback
		fader_counter = 0
		led_pi = pigpio.pi()
		while True:
			if self.fader_mode:
				# fader
				if fader_counter % fader_scale == 0:
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

					led_pi.set_PWM_dutycycle(RED_PIN, r)
					led_pi.set_PWM_dutycycle(GREEN_PIN, g)
					led_pi.set_PWM_dutycycle(BLUE_PIN, b)

					degrees = (degrees + 1)%360

				fader_counter = (fader_counter + 1)%(fader_scale*256)

			if self.counter != self.last_counter:
				self.last_counter = self.counter
				self.rotary_callback(self.counter)

	def short_press(self):
		self.sw_short_callback()

	def long_press(self):
		self.sw_long_callback()
