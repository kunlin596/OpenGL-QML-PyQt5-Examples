import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication, QOpenGLVersionProfile, QSurfaceFormat
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import qmlRegisterType

from _003_3d_rotating_triangle.triangle import TriangleUnderlay
import platform

if __name__ == '__main__':
	# Not working in Ubuntu 16.04, result in 1282 error for simple calling like glViewport(...)
	# TODO

	if platform.uname().system == 'Darwin':
		f = QSurfaceFormat()
		f.setVersion(4, 1)
		f.setDepthBufferSize(1) # fix depth buffer error
		f.setStencilBufferSize(1) # fix stencil buffer error

		# If CoreProfile is used, all the other QML rendering will fail, because they only use 2.1
		f.setProfile(QSurfaceFormat.CompatibilityProfile)
		QSurfaceFormat.setDefaultFormat(f)

	qmlRegisterType(TriangleUnderlay, 'OpenGLUnderQml', 1, 0, 'TriangleUnderlay')

	app = QGuiApplication(sys.argv)

	view = QQuickView()
	view.setFormat(f)
	view.setPersistentSceneGraph(True)
	view.setPersistentOpenGLContext(True)
	view.setResizeMode(QQuickView.SizeRootObjectToView)  # Set for the object to resize correctly
	view.setSource(QUrl('TriangleWindow.qml'))
	view.show()

	app.exec()
