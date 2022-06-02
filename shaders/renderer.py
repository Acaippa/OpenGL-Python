import pygame
from OpenGL.GL import*
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

class Renderer:# TODO: create functions for uploading to the shader in the renderer class instead of having them in the main game module.
	def __init__(self, vertex_file, fragment_file):
		with open(vertex_file, "r") as file:
			self.vertex_src = file.read()
			file.close()

		with open(fragment_file, "r") as file:
			self.fragment_src = file.read()
			file.close()

		self.shader = compileProgram(compileShader(self.vertex_src, GL_VERTEX_SHADER), compileShader(self.fragment_src, GL_FRAGMENT_SHADER))

		glUseProgram(self.shader)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)
		glCullFace(GL_BACK)

	def get_id(self):
		return self.shader

class StaticShader(Renderer):
	def __init__(self):
		super().__init__("shaders/vertex_shader.txt", "shaders/fragment_shader.txt")

	def prepare(self):
		glClearColor(0.2, 0.2, 0.2, 1)
		glClear(GL_COLOR_BUFFER_BIT)
		glClear(GL_DEPTH_BUFFER_BIT)
