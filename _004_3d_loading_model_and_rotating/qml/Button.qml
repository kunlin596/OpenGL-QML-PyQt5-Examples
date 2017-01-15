import QtQuick 2.0
//import OpenGLUnderQml 1.0
import QtGraphicalEffects 1.0

Rectangle {
    width: 100
    height: 50

    property alias text: text.text
    property alias mouse_area: mouse_area

    color: Qt.rgba(0.2, 0.2, 0.2, 1.0)

    Behavior on width { NumberAnimation { duration: 30 } }

    Text {
        id: text
        text: 'Button'
        anchors.centerIn: parent
        font.pointSize: 10
        color: 'white'
    }

    MouseArea {
        id: mouse_area

        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            parent.width = 120;
            parent.color = Qt.rgba(0.0, 0.2, 0.8, 1.0)
        }

        onExited: {
            parent.width = 100;
            parent.color = Qt.rgba(0.2, 0.2, 0.2, 1.0)
        }

        onClicked: { }
    }
}