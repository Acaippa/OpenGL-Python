import pygame 
from modules.ObjLoader import*
from modules.TextureLoader import* 
from OpenGL.GL import*
import pyrr
import math
import numpy

class Entity:
	def __init__(self, obj_file, shader, texture="images/me.png"):
		self.model_mesh, self.model_buffer = ObjLoader.load_model(obj_file)
		self.VAO = glGenVertexArrays(1)
		self.VBO = glGenBuffers(1)
		self.shader = shader

		self.texture = glGenTextures(1)
		load_texture_pygame(texture, self.texture)

		glBindVertexArray(self.VAO)

		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBufferData(GL_ARRAY_BUFFER, self.model_buffer.nbytes, self.model_buffer, GL_STATIC_DRAW)

		glEnableVertexAttribArray(0)
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.model_buffer.itemsize * 8, ctypes.c_void_p(0))

		glEnableVertexAttribArray(1)
		glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.model_buffer.itemsize * 8, ctypes.c_void_p(12))

		glEnableVertexAttribArray(2)
		glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.model_buffer.itemsize * 8, ctypes.c_void_p(20))

		glBindVertexArray(0)
		
		self.x, self.y, self.z = 0, 0, 0
		self.rot_x, self.rot_y, self.rot_z = 0, 0, 0

		self.model = pyrr.matrix44.create_from_translation([self.x, self.y, self.z])

		self.model_loc = glGetUniformLocation(self.shader, "model")


	def instanced_draw(self, *args, **kwargs):
		model = pyrr.matrix44.create_from_translation(vec3_pos)
		rotation_x = pyrr.matrix44.create_from_x_rotation(math.radians(vec3_rot[0]))

		model = pyrr.matrix44.multiply(model, rotation_x)

		glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)

		self.draw()

	def get_boundries(self):
		list_ = [list(self.model_buffer[i*8:i*8+3]) for i in range(len(self.model_buffer) // 8)]
		return max(list_), min(list_)


	def draw(self):
		glBindVertexArray(self.VAO)
		glBindTexture(GL_TEXTURE_2D, self.texture)
		# glDrawElements(GL_TRIANGLES, self.model_buffer.itemsize, GL_UNSIGNED_INT, 0)

		self.model = pyrr.matrix44.create_from_translation([self.x, self.y, self.z])

		# Multiply the Matrices for all the axises of rotation.
		self.rotation_x = pyrr.matrix44.create_from_x_rotation(math.radians(self.rot_x))
		self.model = pyrr.matrix44.multiply(self.model, self.rotation_x)

		self.rotation_y = pyrr.matrix44.create_from_y_rotation(math.radians(self.rot_y))
		self.model = pyrr.matrix44.multiply(self.model, self.rotation_y)

		self.rotation_z = pyrr.matrix44.create_from_z_rotation(math.radians(self.rot_z))
		self.model = pyrr.matrix44.multiply(self.model, self.rotation_z)

		glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.model)
		# Make sure this is here or else the wrong entity moves for some reason.
		glDrawArrays(GL_TRIANGLES, 0, len(self.model_mesh))