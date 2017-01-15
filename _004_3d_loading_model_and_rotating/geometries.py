import numpy as np
import pyassimp as ai


class BaseGeometry(object):
	def __init__ (self):
		self.id = -1
		self.vertices = None
		self.colors = None
		self.indices = None
		self.rotation = np.identity(3)
		self.translation = np.array([0.0, 0.0, 0.0])

		self._scene = None
		self._mesh = None

	def read (self, path):
		try:
			self._scene = ai.load(path)
			self._mesh = self._scene.meshes[0]
			self.vertices = self._mesh.vertices
			self.indices = self._mesh.faces.flatten()
			self.colors = self._mesh.colors

		except Exception as e:
			print('Geometry reading error', e)

	def __del__ (self):
		ai.release(self._scene)

	def rotate (self, axis, angle):
		pass

	def translate (self, vec):
		pass

	def update (self):
		"""
		Update the data (position, color)
		:return:
		"""
		pass

	def change_color (self, color):
		if (0.0 < color) and (color < 1.0):
			self.color = [color for i in range(len(self.vertices))]


class Cube(BaseGeometry):
	file_path = 'cube.obj'

	def __init__ (self):
		super(Cube, self).__init__()
		self.length = 1.0
		self.width = 1.0
		self.height = 1.0
		self.read(Cube.file_path)

	def update (self):
		for i in range(0, len(self.vertices), 3):
			self.vertices[i] = self.length if self.vertices[i] > 0 else -self.length
			self.vertices[i + 1] = self.width if self.vertices[i + 1] > 0.0 else -self.width
			self.vertices[i + 2] = self.height if self.vertices[i + 2] > 0.0 else -self.height

	def update_length (self, val):
		self.length = val
		self.update()

	def update_width (self, val):
		self.width = val
		self.update()

	def update_height (self, val):
		self.height = val
		self.update()


class Sphere(BaseGeometry):
	file_path = 'bunny.obj'

	def __init__ (self):
		super(Sphere, self).__init__()
		self.radius = 1.0
		self.stretch_rate = 1.0

		self.stretch_x = 1.0
		self.stretch_y = 1.0
		self.stretch_z = 1.0

		self.read(Sphere.file_path)

	def update_radius (self, val):
		self.radius = val
		self.stretch_rate = val / self.radius
		self.update()

	def update (self):
		self.stretch_rate = self.radius
		for i in range(0, len(self.vertices), 3):
			self.vertices[i] *= (self.stretch_rate * self.stretch_x)
			self.vertices[i + 1] *= (self.stretch_rate * self.stretch_y)
			self.vertices[i + 2] *= (self.stretch_rate * self.stretch_z)

	def update_stretch_x (self, val):
		self.stretch_x = val
		self.update()

	def update_stretch_y (self, val):
		self.stretch_y = val
		self.update()

	def update_stretch_z (self, val):
		self.stretch_z = val
		self.update()


class Axis(BaseGeometry):
	def __init__ (self):
		super(Axis, self).__init__()
		self.vertices = np.array([[-5.0, 0.0, 5.0],  # 0
		                          [5.0, 0.0, 5.0],  # 1
		                          [5.0, 0.0, -5.0],  # 2
		                          [-5.0, 0.0, -5.0]])  # 3
		self.indices = np.array([0, 1, 2, 0, 3, 2])
		self.colors = np.array([[1.0, 0.0, 0.0],
		                        [0.0, 1.0, 0.0],
		                        [0.0, 0.0, 1.0],
		                        [1.0, 1.0, 1.0]])
