import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication, QOpenGLVersionProfile, QSurfaceFormat
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import qmlRegisterType

from _003_3d_rotating_triangle.triangle import TriangleUnderlay

if __name__ == '__main__':
	# Not working in Ubuntu 16.04, result in 1282 error for simple calling like glViewport(...)
	# TODO
	# f = QSurfaceFormat()
	# f.setVersion(4, 1)
	# f.setProfile(QSurfaceFormat.CoreProfile)
	# f.setDepthBufferSize(1)
	# QSurfaceFormat.setDefaultFormat(f)

	qmlRegisterType(TriangleUnderlay, 'OpenGLUnderQml', 1, 0, 'TriangleUnderlay')

	app = QGuiApplication(sys.argv)

	view = QQuickView()
	view.setResizeMode(QQuickView.SizeRootObjectToView)  # Set for the object to resize correctly
	view.setSource(QUrl('TriangleWindow.qml'))
	view.show()

	app.exec()
