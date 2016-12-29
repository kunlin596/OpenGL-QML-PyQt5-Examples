import numpy as np
import numpy.linalg as la
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtQml import QQmlListProperty
import math


def normalize_vector ( v ):
	return v / la.norm(v)


class Camera(QObject):
	eye_changed = pyqtSignal(name = 'eye_changed')
	up_changed = pyqtSignal(name = 'up_changed')
	target_changed = pyqtSignal(name = 'target_changed')

	def __init__ ( self, parent = None ):
		super(Camera, self).__init__(parent)
		self._eye = np.array([0.0, 0.0, 30.0])
		self._up = np.array([0.0, 1.0, 0.0])
		self._target = np.array([0.0, 0.0, -20.0])
		self.x = None
		self.y = None
		self.z = None

		self.mouse_x = 0.0
		self.mouse_y = 0.0
		self._m = np.identity(4)
		self.update_view_matrix()

	def get_view_matrix ( self ):
		# return self._m
		# TODO camera matrix is still buggy, to fix at next example
		m = np.identity(4)
		m[2][3] = -20.0
		return m

	def update_view_matrix ( self ):
		self.z = normalize_vector(self._target - self._eye)  # positive z is pointing at screen
		self.x = normalize_vector(np.cross(self._up, self.z))
		self.y = np.cross(self.z, self.x)

		self._m[0, :] = np.array([self.x[0], self.x[1], self.x[2], 0.0])
		self._m[1, :] = np.array([self.y[0], self.y[1], self.y[2], 0.0])
		self._m[2, :] = np.array([self.z[0], self.z[1], self.z[2], 0.0])
		self._m[3, :] = np.array([self._eye[0], self._eye[1], self._eye[2], 1.0])

	# TODO Will be implemented in the next version
	#
	# @pyqtSlot('float', name = 'move_vertically')
	# def move_vertically ( self, y ):
	# 	self._eye += y * normalize_vector(self.y)
	# 	self.update_view_matrix()
	#
	# @pyqtSlot('float', name = 'move_horizontally')
	# def move_horizontally ( self, x ):
	# 	self._eye += x * normalize_vector(self.x)
	# 	self.update_view_matrix()
	#
	# @pyqtSlot('float', name = 'move_horizontally')
	# def move_forward ( self, z ):
	# 	self._eye += z * normalize_vector(self.z)
	# 	self.update_view_matrix()
	#
	# @pyqtSlot()
	# def rotate_horizontally ( self ):
	# 	pass
	#
	# @pyqtSlot()
	# def rotate_vertically ( self ):
	# 	pass
	#
	# @pyqtProperty(QQmlListProperty, notify = eye_changed)
	# def eye ( self ):
	# 	return self._eye
	#
	# @eye.setter
	# def eye ( self, eye ):
	# 	self._eye = eye
	#
	# @pyqtProperty(QQmlListProperty, notify = up_changed)
	# def up ( self ):
	# 	return self._up
	#
	# @up.setter
	# def up ( self, up ):
	# 	self._up = up
	#
	# @pyqtProperty(QQmlListProperty, notify = target_changed)
	# def target ( self ):
	# 	return self._target
	#
	# @target.setter
	# def target ( self, target ):
	# 	self._target = target


# Tested against glm::perspective
def perspective_projection ( fovy, aspect_ratio, near_z, far_z ):
	m = np.zeros(shape = (4, 4))

	t = near_z * math.tan(fovy / 2.0)  # half width
	r = t * aspect_ratio  # half height

	m[0][0] = near_z / r
	m[1][1] = near_z / t
	m[2][2] = -(far_z + near_z) / (far_z - near_z)
	m[2][3] = -2 * far_z * near_z / (far_z - near_z)
	m[3][2] = -1

	return m


# assuming the volume is symmetric such that no need to specify l, r, t, b
# Tested against glm::ortho(l, r, b, t, near_z, far_z) with
# glm::mat4 p = glm::ortho(-320.0f, 320.0f, -240.0f, 240.0f, 0.001f, 100.0f);
# TODO should be farther tested
def orthographic_projection ( w, h, near_z, far_z ):
	m = np.zeros(shape = (4, 4))

	m[0][0] = 2.0 / w
	m[1][1] = 2.0 / h
	m[2][2] = -2.0 / (far_z - near_z)
	m[2][3] = -(far_z + near_z) / (far_z - near_z)
	m[3][3] = 1

	return m
