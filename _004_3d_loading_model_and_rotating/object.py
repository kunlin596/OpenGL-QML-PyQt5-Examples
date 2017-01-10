from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QOpenGLShaderProgram, QOpenGLShader, QMatrix4x4, QOpenGLContext
from _003_3d_rotating_triangle.utils import *
from _003_3d_rotating_triangle.utils import Camera

import platform as pf
import sys

import pyassimp as ai

if pf.uname().system == 'Linux':
	try:
		import OpenGL.GL as GL
	except ImportError as e:
		GL = None
		print('can\'t import OpenGL')
		sys.exit(1)


class ModelUnderlay(QQuickItem):
	theta_changed = pyqtSignal(name = 'theta_changed')  # the optional unbound notify signal. Probably no need herel

	def __init__ ( self, parent = None ):
		super(ModelUnderlay, self).__init__(parent)
		self._renderer = None
		self.windowChanged.connect(self.onWindowChanged)

		self._theta = 0.0

	# @pyqtSlot('QQuickWindow'), incompatible connection error, don't know why
	def onWindowChanged ( self, window ):
		# Because it's in different thread which required a direct connection
		# window == self.window(), they are pointing to the same window instance. Verified.
		window.beforeSynchronizing.connect(self.sync, type = Qt.DirectConnection)
		window.setClearBeforeRendering(False)  # otherwise quick would clear everything we render

	@pyqtSlot(name = 'sync')
	def sync ( self ):
		if self._renderer is None:
			self._renderer = ModelUnderlayRenderer()
			self.window().beforeRendering.connect(self._renderer.paint, type = Qt.DirectConnection)
		self._renderer.set_viewport_size(self.window().size() * self.window().devicePixelRatio())
		self._renderer.set_window(self.window())
		self._renderer.set_theta(self._theta)
		self._renderer.set_projection_matrix()

	@pyqtSlot(int)
	def changeColor ( self, color_enum ):
		# if color_enum == 1:
		# 	colors = colors_red
		# elif color_enum == 2:
		# 	colors = colors_green
		# elif color_enum == 3:
		# 	colors = colors_blue
		# elif color_enum == 4:
		# 	colors = colors_mixed
		pass

	@pyqtProperty('float', notify = theta_changed)
	def theta ( self ):
		return self._theta

	@theta.setter
	def theta ( self, theta ):
		if theta == self._theta:
			return
		self._theta = theta
		self.theta_changed.emit()

		if self.window():
			self.window().update()


class ModelUnderlayRenderer(QObject):
	def __init__ ( self, parent = None ):
		super(ModelUnderlayRenderer, self).__init__(parent)
		self._shader_program = None
		self._viewport_size = QSize()
		self._window = None
		self._camera = Camera()

		self._scene = ai.load('bunny.obj')
		self._mesh = self._scene.meshes[0]
		assert (len(self._mesh))
		self._vertices = self._mesh.vertices[0]
		assert (len(self._vertices))
		self._colors = self._mesh.colors[0]
		assert (len(self._colors))

		self._perspective_projection_matrix = perspective_projection(45.0, 4.0 / 3.0,
		                                                             0.001, 100.0)

		self._orthographic_projection_matrix = orthographic_projection(640.0, 480.0,
		                                                               0.001, 100.0)

		self._model_matrix = np.identity(4)

		self._projection_type = 0
		self._projection_matrix = self._perspective_projection_matrix

		self._theta = 0.0

	def __del__ ( self ):
		ai.release(self._scene)

	def set_theta ( self, theta ):
		self._theta = theta

	# around y axis
	def build_rotation_matrix ( self ):
		m = np.identity(4)
		m[0][0] = np.cos(np.radians(self._theta))
		m[0][2] = np.sin(np.radians(self._theta))
		m[2][0] = -np.sin(np.radians(self._theta))
		m[2][2] = np.cos(np.radians(self._theta))
		return m

	@pyqtSlot(int)
	def setProjectionType ( self, t ):
		if t != self._projection_type:
			self._projection_type = t

	@pyqtSlot()
	def paint ( self ):
		# for Darwin, it's a must
		if pf.uname().system == 'Darwin':
			global GL
			GL = self._window.openglContext().versionFunctions()

		w = self._viewport_size.width()
		h = self._viewport_size.height()

		# x, y
		#     Specify the lower left corner of the viewport rectangle,
		#     in pixels. The initial value is (0,0).
		# width, height
		#     Specify the width and height
		#     of the viewport.
		#     When a GL context is first attached to a window,
		#     width and height are set to the dimensions of that
		#     window.
		GL.glViewport(0, 0, int(w), int(h))

		if self._shader_program is None:
			self._shader_program = QOpenGLShaderProgram()
			self._shader_program.addShaderFromSourceFile(QOpenGLShader.Vertex, 'shaders/OpenGL_2_1/vertex.glsl')
			self._shader_program.addShaderFromSourceFile(QOpenGLShader.Fragment, 'shaders/OpenGL_2_1/fragment.glsl')
			self._shader_program.bindAttributeLocation('position', 0)
			self._shader_program.bindAttributeLocation('color', 1)
			self._shader_program.link()

		self._shader_program.bind()
		self._shader_program.enableAttributeArray(0)
		self._shader_program.enableAttributeArray(1)

		self._shader_program.setAttributeArray(0, self._vertices)
		self._shader_program.setAttributeArray(1, self._colors)

		if self._projection_type == 0:
			self._projection_matrix = self._perspective_projection_matrix
		elif self._projection_type == 1:
			self._projection_matrix = self._orthographic_projection_matrix

		self._model_matrix = self.build_rotation_matrix()

		self._shader_program.setUniformValue('model_matrix',
		                                     QMatrix4x4(self._model_matrix.flatten().tolist()))

		self._shader_program.setUniformValue('view_matrix',
		                                     QMatrix4x4(self._camera.get_view_matrix().flatten().tolist()))

		self._shader_program.setUniformValue('projection_matrix',
		                                     QMatrix4x4(self._projection_matrix.flatten().tolist()))

		GL.glClearColor(0.2, 0.2, 0.2, 1)
		GL.glEnable(GL.GL_DEPTH_TEST)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT)
		GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

		self._shader_program.disableAttributeArray(0)
		self._shader_program.disableAttributeArray(1)

		self._shader_program.release()

		# Restore the OpenGL state for QtQuick rendering
		self._window.resetOpenGLState()
		self._window.update()

	def set_viewport_size ( self, size ):
		self._viewport_size = size

	def set_window ( self, window ):
		self._window = window

	def set_projection_matrix ( self ):
		# Need to be set every time we change the size of the window
		self._perspective_projection_matrix = perspective_projection(45.0,
		                                                             self._viewport_size.width() / self._viewport_size.height(),
		                                                             0.001, 100.0)

		self._orthographic_projection_matrix = orthographic_projection(self._viewport_size.width(),
		                                                               self._viewport_size.height(),
		                                                               0.001, 100.0)
