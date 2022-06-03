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
		pygame.mouse.set_cursor((8,8),(1,1),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

		self.shader = StaticShader()
		self.camera = Camera(self.width, self.height)
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
			self.camera.process_mouse_movement(mouse_pos[0], mouse_pos[1])
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