from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QOpenGLShaderProgram, QOpenGLShader, QMatrix4x4, QOpenGLContext
from _004_3d_loading_model_and_rotating.utils import *
from _004_3d_loading_model_and_rotating.utils import Camera
from _004_3d_loading_model_and_rotating.geometries import Cube, Sphere, Axis

import random
import sys
import numpy as np
import platform as pf

theta = 0.0

if pf.uname().system == 'Linux':
	try:
		import OpenGL.GL as GL
	except ImportError as e:
		GL = None
		print('can\'t import OpenGL')
		sys.exit(1)


class Entity(object):
	def __init__ (self):
		pass


class ModelUnderlay(QQuickItem):
	theta_changed = pyqtSignal(name = 'theta_changed')  # the optional unbound notify signal. Probably no need herel

	def __init__ (self, parent = None):
		super(ModelUnderlay, self).__init__(parent)
		self._renderer = None
		self.windowChanged.connect(self.onWindowChanged)

		self._theta = 0.0

	# @pyqtSlot('QQuickWindow'), incompatible connection error, don't know why
	def onWindowChanged (self, window):
		# Because it's in different thread which required a direct connection
		# window == self.window(), they are pointing to the same window instance. Verified.
		window.beforeSynchronizing.connect(self.sync, type = Qt.DirectConnection)
		window.setClearBeforeRendering(False)  # otherwise quick would clear everything we render

	@pyqtSlot(name = 'sync')
	def sync (self):
		if self._renderer is None:
			self._renderer = ModelUnderlayRenderer()
			self.window().beforeRendering.connect(self._renderer.paint, type = Qt.DirectConnection)
		self._renderer.set_viewport_size(self.window().size() * self.window().devicePixelRatio())
		self._renderer.set_window(self.window())
		self._renderer.set_projection_matrix()

	@pyqtSlot(int)
	def changeColor (self, color_enum):
		# if color_enum == 1:
		# 	colors = colors_red
		# elif color_enum == 2:
		# 	colors = colors_green
		# elif color_enum == 3:
		# 	colors = colors_blue
		# elif color_enum == 4:
		# 	colors = colors_mixed
		pass

	@pyqtSlot(int)
	def add_geometry (self, geo_enum):
		self._renderer.add_geometry(geo_enum)

	@pyqtSlot(int)
	def delete_geometry (self, index):
		self._renderer.delete_geometry(index)

	@pyqtSlot(int)
	def select_obj (self, index = 0):
		pass

	@pyqtSlot(float)
	def stretch_x (self, x):
		pass

	@pyqtSlot(float)
	def stretch_y (self, y):
		pass

	@pyqtSlot(float)
	def stretch_z (self, z):
		pass

	@pyqtSlot(int, int)
	def rotate_obj (self, x, y):
		pass

	@pyqtSlot(int, int)
	def rotate_camera (self, x, y):
		pass

	@pyqtSlot(int)
	def move_camera (self, key):
		"""
		Use keyboard to control camera
		:param key:
		:return:
		"""
		if key == 0:
			self._renderer.move_model(10)
		elif key == 1:
			self._renderer.move_model(-10)


class ModelUnderlayRenderer(QObject):
	def __init__ (self, parent = None):
		super(ModelUnderlayRenderer, self).__init__(parent)

		self._shader_program = None
		self._viewport_size = QSize()
		self._window = None
		self._camera = Camera()

		self._perspective_projection_matrix = None
		self._orthographic_projection_matrix = None

		self._model_matrix = np.identity(4)

		self._projection_type = 0
		self._projection_matrix = self._perspective_projection_matrix

		self._index_buffer = -1

		# keep track of the objects in the scene
		self._cube_model = Cube()
		self._sphere_model = Sphere()

		self._models = {}
		self._models[self._cube_model] = []
		self._models[self._sphere_model] = []

	@pyqtSlot()
	def paint (self):
		# for Darwin, it's a must
		if pf.uname().system == 'Darwin':
			global GL
			GL = self._window.openglContext().versionFunctions()

		w = self._viewport_size.width()
		h = self._viewport_size.height()

		GL.glViewport(0, 0, int(w), int(h))
		GL.glClearColor(0.1, 0.1, 0.1, 1)
		GL.glEnable(GL.GL_DEPTH_TEST)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT)
		GL.glClear(GL.GL_DEPTH_BUFFER_BIT)

		if self._shader_program is None:
			self._shader_program = QOpenGLShaderProgram()
			self._shader_program.addShaderFromSourceFile(QOpenGLShader.Vertex, 'shaders/OpenGL_2_1/vertex.glsl')
			self._shader_program.addShaderFromSourceFile(QOpenGLShader.Fragment, 'shaders/OpenGL_2_1/fragment.glsl')
			self._shader_program.bindAttributeLocation('position', 0)
			self._shader_program.bindAttributeLocation('color', 1)
			self._shader_program.link()

		vertices_block = np.array(self._cube_model.vertices)
		colors_block = np.array(self._cube_model.colors)

		if len(self._objects) > 1:
			for v in self._vertices[1:]:
				vertices_block = np.vstack((vertices_block, v))
			for idx, c in enumerate(self._colors[1:]):
				if not c:
					c = [[0.6, 0.6, 0.7] for i in range(len(self._vertices[idx]))]
				colors_block = np.vstack((colors_block, c))
			for i in self._indices[1:]:
				indices_block = np.hstack((indices_block, i))

		self._shader_program.bind()
		self._shader_program.enableAttributeArray(0)
		self._shader_program.setAttributeArray(0, vertices_block)

		self._shader_program.enableAttributeArray(1)
		self._shader_program.setAttributeArray(1, colors_block)

		self._projection_matrix = self._perspective_projection_matrix

		def build_rotation_matrix (t):
			m = np.identity(4)
			m[0][0] = np.cos(np.radians(t))
			m[0][2] = np.sin(np.radians(t))
			m[2][0] = -np.sin(np.radians(t))
			m[2][2] = np.cos(np.radians(t))
			return m

		global theta
		theta += 1
		self._model_matrix = build_rotation_matrix(theta)
		self._model_matrix[2][3] = -3

		view_matrix = np.identity(4)
		# view_matrix = self._camera.get_view_matrix()
		view_matrix[2][3] = -30

		self._shader_program.setUniformValue('model_matrix',
		                                     QMatrix4x4(self._model_matrix.flatten().tolist()))
		self._shader_program.setUniformValue('view_matrix',
		                                     QMatrix4x4(view_matrix.flatten().tolist()).transposed())
		self._shader_program.setUniformValue('projection_matrix',
		                                     QMatrix4x4(self._projection_matrix.flatten().tolist()).transposed())

		GL.glDrawElements(GL.GL_TRIANGLES, len(indices_block), GL.GL_UNSIGNED_INT, indices_block.tolist())
		# GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(indices_block))

		self._shader_program.disableAttributeArray(0)
		self._shader_program.disableAttributeArray(1)

		self._shader_program.release()

		# Restore the OpenGL state for QtQuick rendering
		self._window.resetOpenGLState()
		self._window.update()

	def set_viewport_size (self, size):
		self._viewport_size = size

	def set_window (self, window):
		self._window = window

	def set_projection_matrix (self):
		# Need to be set every time we change the size of the window
		self._perspective_projection_matrix = perspective_projection(45.0,
		                                                             self._window.width() / self._window.height(),
		                                                             0.001, 1000.0)

	def move_model (self, val):
		self._model_matrix[2][3] += val

	def move_camera (self):
		pass

	def add_geometry (self, geo_enum):
		obj = None
		if geo_enum == 0:
			obj = Cube()
		elif geo_enum == 1:
			obj = Sphere()
		elif geo_enum == 2:
			obj = Axis()
		else:
			return

		self._objects.append(obj)
		self._vertices.append(obj.vertices)
		self._colors.append(obj.colors)
		self._indices.append(obj.indices)

		obj.id = len(self._objects) - 1

	def delete_geometry (self, i = 0):
		if self._objects:
			self._vertices.pop(i)
			self._colors.pop(i)
			self._indices.pop(i)
			self._objects.pop(i)
