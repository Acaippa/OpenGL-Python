import OpenGL.GL
from pyrr import*
import numpy as np


class Light:
	def __init__(self, pos, color, brightness):
		self.position = np.array(pos)
		self.color = color
		self.brightness = 0.01 * brightness

	def get_pos(self):
		return self.position

	def set_pos(self, pos):
		self.position = pos

	def get_color(self):
		return self.color

	def set_color(self, color):
		self.color = color

	def get_brightness(self):
		return self.brightness

	def set_brightness(self, brightness):
		self.brightness = brightness

