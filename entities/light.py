import OpenGL.GL
from pyrr import*
import numpy as np


class Light:
	def __init__(self, pos, color):
		self.position = np.array(pos)
		self.color = color

	def get_pos(self):
		return self.position

	def set_pos(self, pos):
		self.position = pos

	def get_color(self):
		return self.color

	def set_color(self, color):
		self.color = color