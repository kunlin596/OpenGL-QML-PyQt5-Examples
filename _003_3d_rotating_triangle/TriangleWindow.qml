import QtQuick 2.0
import OpenGLUnderQml 1.0
import QtGraphicalEffects 1.0

Item {
    width: 640
    height: 320

    TriangleUnderlay {
        id: triangle
    }

    Rectangle {
        id: button1

        width: 200
        height: 50

        color: Qt.rgba(0.9, 0.1, 0.1, 1.0)

        anchors.right: parent.right


        Behavior on width { NumberAnimation { duration: 100 } }

        Text {
            text: 'Red'
            anchors.centerIn: parent
            font.pointSize: 20
            color: 'white'
        }

        MouseArea
        {
            anchors.fill: parent
            hoverEnabled: true

            onEntered: {
                button1.width = 210
            }

            onExited: {
                button1.width = 190
            }

            onClicked: {
                triangle.changeColor(1)
            }
        }
    }

    Rectangle {
        id: button2

        width: 200
        height: 50

        color: Qt.rgba(0.1, 1.0, 0.1, 1.0)

        anchors.top: button1.bottom
        anchors.right: parent.right


        Behavior on width { NumberAnimation { duration: 100 } }

        Text {
            text: 'Green'
            anchors.centerIn: parent
            font.pointSize: 20
            color: 'white'
        }

        MouseArea
        {
            anchors.fill: parent
            hoverEnabled: true

            onEntered: {
                button2.width = 210
            }

            onExited: {
                button2.width = 190
            }

            onClicked: {
                triangle.changeColor(2)
            }
        }
    }

    Rectangle {
        id: button3

        width: 200
        height: 50


        color: Qt.rgba(0.1, 0.1, 1.0, 1.0)

        anchors.top: button2.bottom
        anchors.right: parent.right


        Behavior on width { NumberAnimation { duration: 100 } }

        Text {
            text: 'Blue'
            anchors.centerIn: parent
            font.pointSize: 20
            color: 'white'
        }

        MouseArea
        {
            anchors.fill: parent
            hoverEnabled: true

            onEntered: {
                button3.width = 210
            }

            onExited: {
                button3.width = 190
            }

            onClicked: {
                triangle.changeColor(3)
            }

        }
    }

    Rectangle {
        id: button4

        width: 200
        height: 50

        anchors.top: button3.bottom
        anchors.right: parent.right


        Behavior on width { NumberAnimation { duration: 100 } }

        LinearGradient {
            anchors.fill: parent
            start: Qt.point(0, 0)
            end: Qt.point(button4.width, 0)
            gradient: Gradient {
                GradientStop { position: 0.0; color: "red" }
                GradientStop { position: 0.5; color: "green" }
                GradientStop { position: 1.0; color: "blue" }
            }
        }

        Text {
            text: '3 Colors'
            anchors.centerIn: parent
            font.pointSize: 20
            color: 'white'
        }

        MouseArea
        {
            anchors.fill: parent
            hoverEnabled: true

            onEntered: {
                button4.width = 210
            }

            onExited: {
                button4.width = 190
            }

            onClicked: {
                triangle.changeColor(4)
            }
        }
    }

}