import numpy as np
import numpy.linalg as la
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtQml import QQmlListProperty
import math


class Camera(object):
	def __init__ (self, parent = None):
		self._eye = np.array([0.0, 0.0, -30.0])
		self._up = np.array([0.0, 1.0, 0.0])
		self._target = np.array([0.0, 0.0, 1.0])
		self.x = None
		self.y = None
		self.z = None

		self.mouse_x = 0.0
		self.mouse_y = 0.0
		self._m = np.identity(4)
		self.update_view_matrix()

	def get_view_matrix (self):
		# m = np.identity(4)
		# m[2][3] = -60.0
		# return m

		print(self._m)

		return self._m

	def get_projection_matrix (self):
		pass

	def update_view_matrix (self):
		# self.z = normalize_vector(self._eye - self._target)  # positive z is pointing at screen
		# self.x = normalize_vector(np.cross(self._up, self.z))
		# self.y = normalize_vector(np.cross(self.z, self.x))
		#
		# self._m[:, 0] = np.array([self.x[0], self.x[1], self.x[2], 0.0])
		# self._m[:, 1] = np.array([self.y[0], self.y[1], self.y[2], 0.0])
		# self._m[:, 2] = np.array([self.z[0], self.z[1], self.z[2], 0.0])
		# self._m[:, 3] = np.array([self._eye[0], self._eye[1], self._eye[2], 1.0])
		self._m = look_at(self._eye, self._eye + self._target, self._up)
		print(self._m)

	@pyqtSlot(float)
	def move_horizontally (self, dist):
		self._eye += dist * normalize_vector(self.x)
		self._target += dist * normalize_vector(self.x)
		self.update_view_matrix()

	@pyqtSlot(float)
	def move_vertically (self, dist):
		self._eye += dist * normalize_vector(self.y)
		self._target += dist * normalize_vector(self.y)
		self.update_view_matrix()

	@pyqtSlot(float)
	def move_forward (self, dist):
		self._eye += dist * normalize_vector(self.z)
		self._target += dist * normalize_vector(self.z)
		self.update_view_matrix()

	@pyqtSlot()
	def rotate_horizontally (self, angle):
		pass

	@pyqtSlot()
	def rotate_vertically (self, angle):
		pass


def perspective_projection (fovy, aspect_ratio, near_z, far_z):
	m = np.zeros(shape = (4, 4))

	t = np.tan(np.radians(fovy) / 2.0)  # half width

	m[0][0] = 1.0 / (aspect_ratio * t)
	m[1][1] = 1.0 / t
	m[2][2] = -(far_z + near_z) / (far_z - near_z)
	m[2][3] = -1.0
	m[3][2] = -(2.0 * far_z * near_z) / (far_z - near_z)

	return m


def look_at (eye, center, up):
	f = normalize_vector(center - eye)
	u = normalize_vector(up)
	s = normalize_vector(np.cross(f, u))
	u = np.cross(s, f)

	m = np.identity(4)

	m[0, :] = np.array([s[0], s[1], s[2], -np.dot(s, eye)])
	m[1, :] = np.array([u[0], u[1], u[2], -np.dot(u, eye)])
	m[2, :] = np.array([-f[0], -f[1], -f[2], np.dot(f, eye)])

	return m


# assuming the volume is symmetric such that no need to specify l, r, t, b
# Tested against glm::ortho(l, r, b, t, near_z, far_z) with
# glm::mat4 p = glm::ortho(-320.0f, 320.0f, -240.0f, 240.0f, 0.001f, 100.0f);
# TODO should be farther tested
def orthographic_projection (w, h, near_z, far_z):
	m = np.zeros(shape = (4, 4))

	m[0][0] = 2.0 / w
	m[1][1] = 2.0 / h
	m[2][2] = -2.0 / (far_z - near_z)
	m[2][3] = -(far_z + near_z) / (far_z - near_z)
	m[3][3] = 1

	return m


def normalize_vector (v):
	return v / la.norm(v)
