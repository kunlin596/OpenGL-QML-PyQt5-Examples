import QtQuick 2.0

Rectangle {
    width: 640
    height: 480

    color: 'black'

    Text {
        text: '001 Simple Window Example'
        anchors {
            left: parent.left
            top: parent.top
            margins: 20
        }

        font.pointSize: 10
        color: 'white'
    }

    Text {
        anchors.centerIn: parent
        //    anchors.fill: parent
        text: 'Hello World!'
        font.pointSize: 30
        color: 'white'
    }
}