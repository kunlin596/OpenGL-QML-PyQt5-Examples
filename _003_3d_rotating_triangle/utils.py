import numpy as np
import numpy.linalg as la
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtQml import QQmlListProperty


def normalize_vector ( v ):
	return v / la.norm(v)


class Camera(QObject):
	eye_changed = pyqtSignal(name = 'eye_changed')
	up_changed = pyqtSignal(name = 'up_changed')
	target_changed = pyqtSignal(name = 'target_changed')

	def __init__ ( self, parent = None ):
		super(Camera, self).__init__(parent)
		self._eye = np.array([0.0, 0.0, -20.0])
		self._up = np.array([0.0, 1.0, 0.0])
		self._target = np.array([0.0, 0.0, 20.0])
		self.x = None
		self.y = None
		self.z = None

		self.mouse_x = 0.0
		self.mouse_y = 0.0
		self._m = np.identity(4)
		self.update_view_matrix()

	@pyqtSlot('float', name = 'move_vertically')
	def move_vertically ( self, y ):
		self._eye += y * normalize_vector(self.y)
		self.update_view_matrix()

	@pyqtSlot('float', name = 'move_horizontally')
	def move_horizontally ( self, x ):
		self._eye += x * normalize_vector(self.x)
		self.update_view_matrix()

	@pyqtSlot('float', name = 'move_horizontally')
	def move_forward ( self, z ):
		self._eye += z * normalize_vector(self.z)
		self.update_view_matrix()

	@pyqtSlot()
	def rotate_horizontally ( self ):
		pass

	@pyqtSlot()
	def rotate_vertically ( self ):
		pass

	def update_view_matrix ( self ):
		self.z = normalize_vector(self._target - self._eye)  # positive z is pointing at screen
		self.x = normalize_vector(np.cross(self._up, self.z))
		self.y = np.cross(self.z, self.x)

		self._m[0, :] = np.array([self.x[0], self.x[1], self.x[2], 0.0])
		self._m[1, :] = np.array([self.y[0], self.y[1], self.y[2], 0.0])
		self._m[2, :] = np.array([self.z[0], self.z[1], self.z[2], 0.0])
		self._m[3, :] = np.array([self._eye[0], self._eye[1], self._eye[2], 1.0])

	def get_view_matrix ( self ):
		return self._m

	@pyqtProperty(QQmlListProperty, notify = eye_changed)
	def eye ( self ):
		return self._eye

	@eye.setter
	def eye ( self, eye ):
		self._eye = eye

	@pyqtProperty(QQmlListProperty, notify = up_changed)
	def up ( self ):
		return self._up

	@up.setter
	def up ( self, up ):
		self._up = up

	@pyqtProperty(QQmlListProperty, notify = target_changed)
	def target ( self ):
		return self._target

	@target.setter
	def target ( self, target ):
		self._target = target


# TODO
def perspective_projection ( ):
	m = np.identity(4)
	return m


# TODO
def orthographic_projection ( ):
	m = np.identity(4)
	return m
