import pygame
from OpenGL.GL import*
from OpenGL.GL.shaders import compileProgram, compileShader
from pyrr import*
from entities.light import*

class Renderer:
	def __init__(self, vertex_file, fragment_file):
		# Loading the vertex and shader files
		with open(vertex_file, "r") as file:
			self.vertex_src = file.read()
			file.close()

		with open(fragment_file, "r") as file:
			self.fragment_src = file.read()
			file.close()

		# Creating the shader program.
		self.shader = compileProgram(compileShader(self.vertex_src, GL_VERTEX_SHADER), compileShader(self.fragment_src, GL_FRAGMENT_SHADER))

		# Using the program and enabling some other important settings.
		glUseProgram(self.shader)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)
		glCullFace(GL_BACK)

	def get_id(self):
		return self.shader

	def get_location(self, item): # Get the location of a uniform variable in the shader.
		return glGetUniformLocation(self.shader, item)

	def store_float_array_at_location(self, location, item): # Upload the uniform value in the shader at the specific location.
		func = eval(f"glUniform{len(item)}f")
		func(location, *item)
		print(*item)

	def store_int_array_at_location(self, location, item):
		func = eval(f"glUniform{len(item)}i")
		func(location, *item)
		print(*item)

	def store_float_at_location(self, location, item): # Upload the uniform value in the shader at the specific location.
		glUniform1f(location, item)

	def store_float_matrix_at_location(self, location, item): # Store a matrix into the shader
		glUniformMatrix4fv(location, 1, GL_FALSE, item)

	def add_light(self, brightness, vec3_pos=[0.0, 0.0, 0.0], vec3_color=[1.0, 1.0, 1.0]): # Creating a light and adding it's position and color to the vertex and fragment shader.
		self.light = Light(vec3_pos, vec3_color, brightness)

		self.light_pos_loc = self.get_location("light_position")
		self.light_color_loc = self.get_location("light_color")
		self.light_brightness_loc = self.get_location("light_brightness")

		self.light_pos = self.light.get_pos()
		self.light_color = self.light.get_color()
		self.light_brightness = self.light.get_brightness()

		self.store_float_array_at_location(self.light_pos_loc, self.light_pos)
		self.store_float_array_at_location(self.light_color_loc, self.light_color)
		self.store_float_at_location(self.light_brightness_loc, self.light_brightness)

		return self.light

	def create_perspective_projection(self, width, height, fov=45, close=0.1, far=1000):
		self.projection = matrix44.create_perspective_projection_matrix(fov, width / height, close, far)
		self.proj_loc = self.get_location("projection")
		self.store_float_matrix_at_location(self.proj_loc, self.projection)

	def change_view_matrix(self, matrix): # Update the view matrix gotten from the camera entity.
		self.view_loc = glGetUniformLocation(self.shader, "view")
		glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, matrix)

	def load_sky_color(self, r, g, b):
		self.fog_loc = self.get_location("sky_color")
		self.store_float_array_at_location(self.fog_loc, Vector3(np.array((r, g, b))))

	def get_projection_matrix(self):
		return self.projection


class StaticShader(Renderer):
	def __init__(self):
		super().__init__("shaders/vertex_shader.txt", "shaders/fragment_shader.txt")

		self.red = 0.2
		self.green = 0.2
		self.blue = 0.2

		super().load_sky_color(self.red, self.green, self.blue)

	def prepare(self):
		glClearColor(self.red, self.green, self.blue, 1)
		glClear(GL_COLOR_BUFFER_BIT)
		glClear(GL_DEPTH_BUFFER_BIT)
