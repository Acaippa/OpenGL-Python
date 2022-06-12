#from entities.camera import*
from pyrr import*
import pygame
import numpy as np

class MousePicker:
	def __init__(self, camera, projection_matrix):
		self.camera = camera
		self.projection_matrix = projection_matrix
		self.view_matrix = self.camera.get_view_matrix()

	def get_current_ray(self):
		return self.calculate_mouse_Ray()

	def update(self):
		self.view_matrix = self.camera.get_view_matrix()

	def calculate_mouse_Ray(self):
		self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
		normalized_coords = self.get_normalized_device_coords(self.mouse_x, self.mouse_y)
		clip_coords = Vector4([normalized_coords[0], normalized_coords[1], -1.0, 1.0])
		eye_coords = self.to_eye_coords(clip_coords)
		world_ray = Vector3(self.to_world_coords(eye_coords))
		return world_ray

	def to_world_coords(self, eye_coords):
		inverted_view = np.linalg.inv(self.view_matrix)
		# change
		ray_world = matrix44.multiply(inverted_view, eye_coords)
		mouse_ray = Vector3([ray_world[0], ray_world[1], ray_world[2]])
		mouse_ray.normalize()
		return mouse_ray


	def to_eye_coords(self, clip_coords):
		inverted_projection = matrix44.inverse(self.projection_matrix)
		# change
		eye_coords = matrix44.multiply(inverted_projection, clip_coords)
		return Vector4([eye_coords[0], eye_coords[1], -1.0, 0.0])		

	def get_normalized_device_coords(self, mouse_x, mouse_y): # Convert the mouse coordinates to a value between 0.0 and 1.0.
		display = pygame.display.get_surface()
		x = mouse_x / display.get_width()
		y = mouse_y / display.get_height()
		return (x, y)

	#TODO: Figure out a way to check if the ray intersects wth any object.

