from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QOpenGLShaderProgram, QOpenGLShader

from OpenGL.GL import *

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

vertex_shader_source = "attribute highp vec3 position;\n" \
                       "attribute highp vec3 color;\n" \
                       "\n" \
                       "varying vec3 pass_color;\n" \
                       "\n" \
                       "void main () {\n" \
                       "    gl_Position = vec4(position, 1.0);\n" \
                       "    pass_color = color;\n" \
                       "}\n"

fragment_shader_source = "varying highp vec3 pass_color;\n" \
                         "\n" \
                         "void main () {\n" \
                         "    gl_FragColor = vec4(pass_color, 1.0);\n" \
                         "}\n"


class TriangleUnderlay(QQuickItem):
	def __init__ ( self, parent = None ):
		super(TriangleUnderlay, self).__init__(parent)
		self._renderer = None
		self.windowChanged.connect(self.onWindowChanged)

	# @pyqtSlot('QQuickWindow'), incompatible connection error, don't know why
	def onWindowChanged ( self, window ):
		# Because it's in different thread which required a direct connection
		# window == self.window(), they are pointing to the same window instance. Verified.
		window.beforeSynchronizing.connect(self.sync, type = Qt.DirectConnection)
		window.setClearBeforeRendering(False)  # otherwise quick would clear everything we render

	@pyqtSlot(name = 'sync')
	def sync ( self ):
		if self._renderer is None:
			self._renderer = TriangleUnderlayRenderer(self)
			# Because it's in different thread which required a direct connection
			self.window().beforeRendering.connect(self._renderer.paint, type = Qt.DirectConnection)
		self._renderer.set_viewport_size(self.window().size() * self.window().devicePixelRatio())
		self._renderer.set_window(self.window())

	@pyqtSlot(int)
	def changeColor ( self, color_enum ):
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
	def __init__ ( self, parent = None ):
		super(TriangleUnderlayRenderer, self).__init__(parent)
		self._shader_program = None
		self._viewport_size = QSize()
		self._window = None

	@pyqtSlot()
	def paint ( self ):
		if self._shader_program is None:
			self._shader_program = QOpenGLShaderProgram()
			self._shader_program.addShaderFromSourceCode(QOpenGLShader.Vertex,
			                                             vertex_shader_source)
			self._shader_program.addShaderFromSourceCode(QOpenGLShader.Fragment,
			                                             fragment_shader_source)
			self._shader_program.bindAttributeLocation('position', 0)
			self._shader_program.bindAttributeLocation('color', 1)
			self._shader_program.link()

		self._shader_program.bind()
		self._shader_program.enableAttributeArray(0)
		self._shader_program.enableAttributeArray(1)

		self._shader_program.setAttributeArray(0, positions)
		self._shader_program.setAttributeArray(1, colors)

		glViewport(0, 0, self._viewport_size.width(), self._viewport_size.height())
		#
		glClearColor(0.5, 0.5, 0.5, 1)
		# glDisable(GL_DEPTH_TEST)

		glClear(GL_COLOR_BUFFER_BIT)

		glDrawArrays(GL_TRIANGLES, 0, 3)

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
