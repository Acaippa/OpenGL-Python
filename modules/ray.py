from OpenGL.GL import*
from pyrr import*

class Ray: # Class that renderers a ray between two points.
	def __init__(self, start, end, time):
		start = Vector3(start)
		end = Vector3([end.x * time, end.y * time, end.z * time])
		end = start + end

		glBegin(GL_LINES)
		glVertex3f(start.x, start.y, start.z)
		glVertex3f(end.x, end.y, end.z)
		glEnd()


