import math
from pyrr import*
from OpenGL.GL import*
import numpy as np
from math import sin, cos, radians
import pygame

# Returns self.view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 10]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

class Camera:
	def __init__(self):
		self.pos = Vector3([-5.0, 0.0, 0.0])
		self.front = Vector3([0.0, 0.0, -1.0])
		self.up = Vector3([0.0, 1.0, 0.0])
		self.right = Vector3([1.0, 0.0, 0.0])

		self.jaw = 0
		self.pitch = 0

		self.speed = 0.5

		self.delta_tick = 1 
		self.delta_time = 1

		self.mouse_sensitivity = 0.25

	def get_view_matrix(self):
		self.delta_time = (pygame.time.get_ticks() - self.delta_tick) / 50
		self.delta_tick = pygame.time.get_ticks()

		return matrix44.create_look_at(self.pos, self.pos + self.front, self.up)

	def process_mouse_movement(self, x_offset, y_offset):
		x_offset *= self.mouse_sensitivity * self.delta_time
		y_offset *= self.mouse_sensitivity * self.delta_time

		self.jaw += x_offset
		self.pitch -= y_offset
		self.update_camera_vectors()


	def update_camera_vectors(self):
		front = Vector3([0.0, 0.0, 0.0])
		front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
		front.y = sin(radians(self.pitch))
		front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

		self.front = vector.normalise(front)
		self.right = vector.normalise(vector3.cross(self.front, Vector3([0.0, 1.0, 0.0])))
		self.up = vector.normalise(vector3.cross(self.right, self.front))

	def process_keyboard(self, type):
		if type == "forward":
			self.pos += self.front * self.speed * self.delta_time

		if type == "backward":
			self.pos -= self.front * self.speed * self.delta_time

		if type == "right":
			self.pos += self.right * self.speed * self.delta_time

		if type == "left":
			self.pos -= self.right * self.speed * self.delta_time