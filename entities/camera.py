import math
from pyrr import*
from OpenGL.GL import*
import numpy as np
from math import sin, cos, radians
import pygame

# Returns self.view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 10]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

class Camera:
	def __init__(self, width, height):
		self.pos = Vector3([-5.0, 0.0, 0.0])
		self.front = Vector3([0.0, 0.0, -1.0])
		self.up = Vector3([0.0, 1.0, 0.0])
		self.right = Vector3([1.0, 0.0, 0.0])

		self.screen_width = width
		self.screen_height = height

		self.far = 1000

		self.jaw = 0
		self.pitch = 0

		self.speed = 0.5

		self.delta_tick = 1 
		self.delta_time = 1

		self.mouse_sensitivity = 0.10

		self.last_x = 0
		self.last_y = 0
		self.x_offset = 0
		self.y_offset = 0

		self.first_mouse = True

		self.restrict_y = True
		self.pitch_restrict = 70

		self.restrict_cursor(True)

		# Center the mouse
		mouse = pygame.mouse.get_pos()
		pygame.mouse.set_pos(self.screen_width // 2, self.screen_height // 2)
		self.mouse_reset = False
		self.mouse_reset_pos = 0

	def get_view_matrix(self):
		return matrix44.create_look_at(self.pos, self.pos + self.front, self.up)

	def reset_mouse_pos(self):
		if self.restrict_cursor_bool:
			pygame.mouse.set_pos(self.screen_width // 2, self.screen_height // 2)

			self.last_x = self.screen_width // 2
			self.x_offset = 0
			self.last_y = self.screen_height // 2
			self.y_offset = 0

	def process_mouse_movement(self, x_pos, y_pos):
		if self.first_mouse: # Set the last position to be the current position of the mouse for the first frame.
			self.last_x = x_pos
			self.last_y = y_pos
			self.first_mouse = False

		if not x_pos >= self.screen_width - 2 and not x_pos <= 2 and not y_pos >= self.screen_height - 2 and not y_pos <= 2:
			self.x_offset = x_pos - self.last_x
			self.y_offset = y_pos - self.last_y

			self.last_x = x_pos
			self.last_y = y_pos

			self.x_offset *= self.mouse_sensitivity
			self.y_offset *= self.mouse_sensitivity

		if self.restrict_cursor_bool: # The camera should not move while the cursor is not restricted.
			# Restricting the pitch.
			if not self.pitch - self.y_offset > self.pitch_restrict and not self.pitch - self.y_offset < self.pitch_restrict * -1:
				self.pitch -= self.y_offset

			self.jaw += self.x_offset

			self.update_camera_vectors()

		self.reset_mouse_pos()


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

	def restrict_cursor(self, bool):
		self.restrict_cursor_bool = bool
		pygame.event.set_grab(bool)

	def camera_movement(self, keys):
			if keys[pygame.K_w]:
					self.process_keyboard("forward")

			if keys[pygame.K_s]:
				self.process_keyboard("backward")

			if keys[pygame.K_d]:
					self.process_keyboard("right")

			if keys[pygame.K_a]:
				self.process_keyboard("left")

	def get_position(self):
		return self.pos + self.front