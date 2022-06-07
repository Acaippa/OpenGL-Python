import pygame
from OpenGL.GL import*
from shaders.renderer import*
from entities.entities import*
from entities.camera import*
import pyrr
import random

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
		# Make the cursor insivible. This should be changed later so we can controll if we want to see the cursor or not.
		pygame.mouse.set_cursor((8,8),(1,1),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

		self.shader = StaticShader()
		self.shader.create_perspective_projection(self.width, self.height)
		self.camera = Camera(self.width, self.height)
		self.light = self.shader.add_light(1.0, [0.0, 100.0, 0.0], [1.0, 1.0, 1.0])

		# Reference the state that should be run in the main loop.
		self.state = GameState(self)

	def run(self):
		self.running = True

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			keys = pygame.key.get_pressed()
			self.camera.camera_movement(keys)
			if keys[pygame.K_ESCAPE]:
				self.running = False


			# DeltaTime setup.
			self.delta_time = (pygame.time.get_ticks() - self.delta_tick) / 50
			self.delta_tick = pygame.time.get_ticks()

			self.state.run()

			# View and camera logic.
			mouse_pos = pygame.mouse.get_pos()
			self.camera.process_mouse_movement(mouse_pos[0], mouse_pos[1])
			self.shader.change_view_matrix(self.camera.get_view_matrix())

			self.clock.tick(60)
			pygame.display.flip()
		

class GameState:
	def __init__(self, parent):
		self.parent = parent

		# Defining an entity that will be used in the "game"
		self.Terrain = Entity("floor.obj", self.parent.shader.get_id(), "images/grass.png")

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

		self.Terrain.draw()



game = Game(1280, 720)
game.run()