import unittest
import numpy as np
import numpy.linalg as la
from _003_3d_rotating_triangle.utils import Camera


class TestCamera(unittest.TestCase):
	def test_camera_lookat ( self ):
		c = Camera()
		c.update_view_matrix()


if __name__ == '__main__':
	unittest.main()
