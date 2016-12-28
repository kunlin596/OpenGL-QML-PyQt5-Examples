from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QOpenGLShaderProgram, QOpenGLShader, QMatrix4x4, QOpenGLContext
from _003_3d_rotating_triangle.utils import *
from _003_3d_rotating_triangle.utils import Camera

positions = [
	(-0.5, -0.8, 0.0),
	(0.5, -0.8, 0.0),
	(0.0, 0.8, 0.0)
]

colors_mixed = [
	(1.0, 0.0, 0.0),
	(0.0, 1.0, 0.0),
	(0.0, 0.0, 1.0)
]

colors_red = [
	(1.0, 0.0, 0.0, 0.0),
	(1.0, 0.1, 0.0, 0.0),
	(1.0, 0.1, 0.1, 0.0)
]

colors_green = [
	(0.0, 1.0, 0.0, 0.0),
	(0.1, 1.0, 0.0, 0.0),
	(0.1, 1.0, 0.1, 0.0)
]
colors_blue = [
	(0.0, 0.0, 1.0, 0.0),
	(0.0, 0.1, 1.0, 0.0),
	(0.1, 0.1, 1.0, 0.0)
]

colors = colors_mixed

class TriangleUnderlay(QQuickItem):
	def __init__ (self, parent = None):
		super(TriangleUnderlay, self).__init__(parent)
		self._renderer = None
		self.windowChanged.connect(self.onWindowChanged)

	# @pyqtSlot('QQuickWindow'), incompatible connection error, don't know why
	def onWindowChanged (self, window):
		# Because it's in different thread which required a direct connection
		# window == self.window(), they are pointing to the same window instance. Verified.
		window.beforeSynchronizing.connect(self.sync, type = Qt.DirectConnection)
		window.setClearBeforeRendering(False)  # otherwise quick would clear everything we render

	@pyqtSlot(name = 'sync')
	def sync (self):
		if self._renderer is None:
			self._renderer = TriangleUnderlayRenderer()
			self.window().beforeRendering.connect(self._renderer.paint, type = Qt.DirectConnection)
		self._renderer.set_viewport_size(self.window().size() * self.window().devicePixelRatio())
		self._renderer.set_window(self.window())

	@pyqtSlot(int)
	def changeColor (self, color_enum):
		global colors
		if color_enum == 1:
			colors = colors_red
		elif color_enum == 2:
			colors = colors_green
		elif color_enum == 3:
			colors = colors_blue
		elif color_enum == 4:
			colors = colors_mixed


class TriangleUnderlayRenderer(QObject):
	def __init__ (self, parent = None):
		super(TriangleUnderlayRenderer, self).__init__(parent)
		self._shader_program = None
		self._viewport_size = QSize()
		self._window = None
		self._camera = Camera()

		# TODO
		self._perspective_projection_matrix = perspective_projection()

		# TODO
		self._orthographic_projection_matrix = orthographic_projection()

		self._model_matrix = np.identity(4)

		self._projection_type = 0
		self._projection_matrix = self._perspective_projection_matrix

	@pyqtSlot(int)
	def setProjectionType (self, t):
		if t != self._projection_type:
			self._projection_type = t

	@pyqtSlot()
	def paint (self):

		# for Darwin, it's a must
		gl = self._window.openglContext().versionFunctions()

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

		self._shader_program.setAttributeArray(0, positions)
		self._shader_program.setAttributeArray(1, colors)

		if self._projection_type == 0:
			self._projection_matrix = self._perspective_projection_matrix
		elif self._projection_type == 1:
			self._projection_matrix = self._orthographic_projection_matrix

		self._shader_program.setUniformValue('model_matrix', QMatrix4x4(self._model_matrix.flatten().tolist()))

		# TODO
		self._shader_program.setUniformValue('view_matrix',
		                                     QMatrix4x4(self._camera.get_view_matrix().flatten().tolist()))

		# TODO
		self._shader_program.setUniformValue('projection_matrix',
		                                     QMatrix4x4(self._projection_matrix.flatten().tolist()))

		gl.glViewport(0, 0, self._viewport_size.width(), self._viewport_size.height())
		gl.glClearColor(0.5, 0.5, 0.5, 1)
		gl.glEnable(gl.GL_DEPTH_TEST)
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)
		gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

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
