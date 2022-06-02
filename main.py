import pygame
from OpenGL.GL import*
from shaders.renderer import*
from entities.entities import*
from entities.camera import*
import pyrr
import random
from entities.light import*

class Game:
	def __init__(self, width, height):
		"""
		Initiate the main game loop. This structure makes the game able to call the .init function in order to change some parameters like size and so on. So make sure to add all settings here so i can change them later.
		"""
		pygame.init()

		self.width = width
		self.height = height

		self.display = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
		self.clock = pygame.time.Clock()
		self.delta_tick = pygame.time.get_ticks()
		pygame.mouse.set_visible(True)
		pygame.event.set_grab(True)

		# Center the mouse
		mouse = pygame.mouse.get_pos()
		pygame.mouse.set_pos(self.width // 2, self.height // 2)
		self.mouse_reset = False
		self.mouse_reset_pos = 0

		self.shader = StaticShader()
		self.camera = Camera()
		self.light = Light([0.0, 2.0, 0.0], [1.0, 1.0, 1.0])

		# Setting up the lights.
		self.light_pos_loc = glGetUniformLocation(self.shader.get_id(), "light_position")
		self.light_color_loc = glGetUniformLocation(self.shader.get_id(), "light_color")
		self.light_pos = self.light.get_pos()
		self.light_color = self.light.get_color()
		glUniform3f(self.light_pos_loc, self.light_pos[0], self.light_pos[1], self.light_pos[2])
		glUniform3f(self.light_color_loc, self.light_color[0], self.light_color[1], self.light_color[2])
		# TODO: move this and many other functions related to shader uniforms to the shader instead of the game loop.

		# Setting the projection for the scene.
		self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
		self.proj_loc = glGetUniformLocation(self.shader.get_id(), "projection")
		glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, self.projection)

		# Reference the state that should be run in the main loop.
		self.state = GameState(self)

		# Set these values in order to make the calculations for the mouse offset work.
		self.first_mouse = True
		self.last_x = self.width // 2
		self.last_y = self.height // 2

	def mouse_look(self, x_pos, y_pos): # Calculate the offset of the mouse and send it to the camera.
		if self.first_mouse:
			self.last_x = x_pos
			self.last_y = y_pos
			self.first_mouse = False

		if not self.mouse_reset: # Check if the mouse is moving from one side of the screen to the other, if so do not apply any offset.
			self.x_offset = x_pos - self.last_x
			self.y_offset = y_pos - self.last_y

			self.last_x = x_pos
			self.last_y = y_pos
		else:
			self.x_offset = 0
			self.last_x = self.mouse_reset_pos
			self.mouse_reset = False

		self.camera.process_mouse_movement(self.x_offset, self.y_offset)


	def change_view_matrix(self, matrix): # Update the view matrix gotten from the camera entity.
		self.view_loc = glGetUniformLocation(self.shader.get_id(), "view")
		glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, matrix)

	def camera_movement(self, keys):
		if keys[pygame.K_w]:
				self.camera.process_keyboard("forward")

		if keys[pygame.K_s]:
			self.camera.process_keyboard("backward")

		if keys[pygame.K_d]:
				self.camera.process_keyboard("right")

		if keys[pygame.K_a]:
			self.camera.process_keyboard("left")


	def run(self):
		self.running = True

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				self.running = False

			self.camera_movement(keys)

			# DeltaTime setup.
			self.delta_time = (pygame.time.get_ticks() - self.delta_tick) / 50
			self.delta_tick = pygame.time.get_ticks()

			self.state.run()

			# View and camera logic.
			mouse_pos = pygame.mouse.get_pos()
			self.mouse_look(mouse_pos[0], mouse_pos[1])
			# Makes you able to look 360 degrees.
			if mouse_pos[0] <= 0:
				self.mouse_reset = True
				self.mouse_reset_pos = self.width
				pygame.mouse.set_pos((self.width - 2, mouse_pos[1]))

			if mouse_pos[0] >= self.width - 1:
				self.mouse_reset = True
				self.mouse_reset_pos = 0
				pygame.mouse.set_pos((1, mouse_pos[1]))

			self.change_view_matrix(self.camera.get_view_matrix())


			self.clock.tick(60)
			pygame.display.flip()
		

class GameState:
	def __init__(self, parent):
		self.parent = parent

		# Defining an entity that will be used in the "game"
		self.Entity = Entity("chibi.obj", self.parent.shader.get_id(), "images/me.png")
		self.Entity1 = Entity("floor.obj", self.parent.shader.get_id(), "images/me.png")

		# Save random locations, later in the code we can reuse the mesh and draw them with different positions and or rotations. 
		# self.pos_list = []
		# for i in range(10):
		# 	self.pos_list.append([random.uniform(0, 5.0), 0.0, 0.0])


	def run(self):
		self.parent.shader.prepare()
		self.dt = self.parent.delta_time

		# Example of how to reuse the mesh without making alot of instances of the same mesh.
		# for item in self.pos_list:
		# 	self.Entity.instanced_draw(item)

		self.Entity.y = -2.0
		self.Entity.draw()
		self.Entity1.draw()


		



game = Game(1280, 720)
game.run()