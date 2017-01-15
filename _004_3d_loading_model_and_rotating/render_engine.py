from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QOpenGLShaderProgram, QOpenGLShader, QMatrix4x4, QOpenGLContext
from _004_3d_loading_model_and_rotating.utils import *
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
	def __init__ (self, model, position, rotation, scale_val):
		self._model = model
		self.position = position
		self.rotation = rotation
		self.scale = scale_val


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

	@pyqtSlot()
	def change_random_cube_color (self):
		self._renderer.change_random_cube_color()

	@pyqtSlot()
	def change_random_sphere_color (self):
		self._renderer.change_random_sphere_color()


class ModelUnderlayRenderer(QObject):
	def __init__ (self, parent = None):
		super(ModelUnderlayRenderer, self).__init__(parent)

		self._cube_shader = None
		self._sphere_shader = None
		self._viewport_size = QSize()
		self._window = None
		self._camera = Camera()

		self._perspective_projection_matrix = None
		self._orthographic_projection_matrix = None

		self._model_matrix = np.identity(4)

		self._projection_type = 0
		self._projection_matrix = perspective_projection(45.0,
		                                                 640.0 / 480.0,
		                                                 0.001, 1000.0)

		self._index_buffer = -1

		# keep track of the objects in the scene
		self._cube_model = Cube()
		self._sphere_model = Sphere()

		self._models = dict()
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
		#
		# vertices_block = np.vstack((self._cube_model.vertices, self._sphere_model.vertices))
		# colors_block = np.vstack((self._cube_model.colors, self._sphere_model))
		#
		# if len(self._objects) > 1:
		# 	for v in self._vertices[1:]:
		# 		vertices_block = np.vstack((vertices_block, v))
		# 	for idx, c in enumerate(self._colors[1:]):
		# 		if not c:
		# 			c = [[0.6, 0.6, 0.7] for i in range(len(self._vertices[idx]))]
		# 		colors_block = np.vstack((colors_block, c))
		# 	for i in self._indices[1:]:
		# 		indices_block = np.hstack((indices_block, i))
		view_matrix = np.identity(4)
		view_matrix[2][3] = -30

		if self._cube_shader is None:
			self._cube_shader = QOpenGLShaderProgram()
			self._cube_shader.addShaderFromSourceFile(QOpenGLShader.Vertex, 'shaders/OpenGL_2_1/vertex.glsl')
			self._cube_shader.addShaderFromSourceFile(QOpenGLShader.Fragment, 'shaders/OpenGL_2_1/fragment.glsl')
			self._cube_shader.bindAttributeLocation('position', 0)
			self._cube_shader.bindAttributeLocation('color', 1)
			self._cube_shader.link()

		self._cube_shader.bind()
		self._cube_shader.enableAttributeArray(0)
		self._cube_shader.enableAttributeArray(1)
		self._cube_shader.setAttributeArray(0, self._cube_model.vertices.tolist())
		self._cube_shader.setAttributeArray(1, self._cube_model.colors.tolist())
		# view_matrix = self._camera.get_view_matrix()
		self._cube_shader.setUniformValue('view_matrix',
		                                  QMatrix4x4(view_matrix.flatten().tolist()).transposed())
		self._cube_shader.setUniformValue('projection_matrix',
		                                  QMatrix4x4(self._projection_matrix.flatten().tolist()).transposed())

		if self._cube_model in self._models.keys():
			for entity in self._models[self._cube_model]:
				m = create_transformation_matrix(entity.position, entity.rotation, entity.scale)
				self._cube_shader.setUniformValue('model_matrix', QMatrix4x4(m.flatten().tolist()))
				GL.glDrawElements(GL.GL_TRIANGLES,
				                  len(self._cube_model.indices),
				                  GL.GL_UNSIGNED_INT,
				                  self._cube_model.indices.tolist())

		self._cube_shader.disableAttributeArray(0)
		self._cube_shader.disableAttributeArray(1)
		self._cube_shader.release()

		if self._sphere_shader is None:
			self._sphere_shader = QOpenGLShaderProgram()
			self._sphere_shader.addShaderFromSourceFile(QOpenGLShader.Vertex, 'shaders/OpenGL_2_1/vertex.glsl')
			self._sphere_shader.addShaderFromSourceFile(QOpenGLShader.Fragment, 'shaders/OpenGL_2_1/fragment.glsl')
			self._sphere_shader.bindAttributeLocation('position', 0)
			self._sphere_shader.bindAttributeLocation('color', 1)
			self._sphere_shader.link()

		self._sphere_shader.bind()
		self._sphere_shader.enableAttributeArray(0)
		self._sphere_shader.enableAttributeArray(1)
		self._sphere_shader.setAttributeArray(0, self._sphere_model.vertices.tolist())
		self._sphere_shader.setAttributeArray(1, self._sphere_model.colors.tolist())
		self._sphere_shader.setUniformValue('view_matrix',
		                                    QMatrix4x4(view_matrix.flatten().tolist()).transposed())
		self._sphere_shader.setUniformValue('projection_matrix',
		                                    QMatrix4x4(self._projection_matrix.flatten().tolist()).transposed())

		if self._sphere_model in self._models.keys():
			for entity in self._models[self._sphere_model]:
				m = create_transformation_matrix(entity.position, entity.rotation, entity.scale)
				self._cube_shader.setUniformValue('model_matrix', QMatrix4x4(m.flatten().tolist()))
				GL.glDrawElements(GL.GL_TRIANGLES,
				                  len(self._sphere_model.indices),
				                  GL.GL_UNSIGNED_INT,
				                  self._sphere_model.indices.tolist())
		self._sphere_shader.disableAttributeArray(0)
		self._sphere_shader.disableAttributeArray(1)
		self._sphere_shader.release()

		# def build_rotation_matrix (t):
		# 	m = np.identity(4)
		# 	m[0][0] = np.cos(np.radians(t))
		# 	m[0][2] = np.sin(np.radians(t))
		# 	m[2][0] = -np.sin(np.radians(t))
		# 	m[2][2] = np.cos(np.radians(t))
		# 	return m
		#
		# global theta
		# theta += 1
		# self._model_matrix = build_rotation_matrix(theta)
		# self._model_matrix[2][3] = -3


		# Restore the OpenGL state for QtQuick rendering
		self._window.resetOpenGLState()
		self._window.update()

	def set_viewport_size (self, size):
		self._viewport_size = size

	def set_window (self, window):
		self._window = window

	def set_projection_matrix (self):
		# Need to be set every time we change the size of the window
		self._projection_matrix = perspective_projection(45.0,
		                                                 self._window.width() / self._window.height(),
		                                                 0.001, 1000.0)

	def move_model (self, val):
		self._model_matrix[2][3] += val

	def move_camera (self):
		pass

	def add_geometry (self, geo_enum):
		if geo_enum == 0:
			self._models[self._cube_model].append(Entity(self._cube_model,
			                                             np.array([random.uniform(-3.0, 3.0),
			                                                       random.uniform(-3.0, 3.0),
			                                                       random.uniform(-20.0, -10.0)]),
			                                             np.array([random.uniform(-45.0, 45.0),
			                                                       random.uniform(-45.0, 45.0),
			                                                       random.uniform(-45.0, 45.0)]),
			                                             np.array([1.0, 1.0, 1.0])))
		elif geo_enum == 1:
			self._models[self._sphere_model].append(Entity(self._sphere_model,
			                                               np.array([random.uniform(-3.0, 3.0),
			                                                         random.uniform(-3.0, 3.0),
			                                                         random.uniform(-20.0, -10.0)]),
			                                               np.array([random.uniform(-30.0, 30.0),
			                                                         random.uniform(-30.0, 30.0),
			                                                         random.uniform(-30.0, 30.0)]),
			                                               np.array([1.0, 1.0, 1.0])))
		else:
			return

	def delete_geometry (self, geo_enum):
		if geo_enum == 0:
			if self._models[self._cube_model]:
				self._models[self._cube_model].pop()
		elif geo_enum == 1:
			if self._models[self._sphere_model]:
				self._models[self._sphere_model].pop()

	def change_random_cube_color (self):
		tmp = self._models[self._cube_model]
		self._models.pop(self._cube_model)
		self._cube_model = Cube()
		self._models[self._cube_model] = tmp

	def change_random_sphere_color (self):
		tmp = self._models[self._sphere_model]
		self._models.pop(self._sphere_model)
		self._sphere_model = Sphere()
		self._models[self._sphere_model] = tmp
