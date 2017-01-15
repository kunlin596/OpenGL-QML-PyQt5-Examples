import QtQuick 2.0
import OpenGLUnderQml 1.0
import QtGraphicalEffects 1.0

Item {
    width: 640
    height: 480

    focus: true
    Keys.onPressed: {
        if (event.key == Qt.Key_W) {
//            scene.move_camera(0);
            event.accepted = true;
            console.log("(w) Move camera forward")
        }
        if (event.key == Qt.Key_S) {
//            scene.move_camera(1);
            event.accepted = true;
            console.log("(s) Move camera backward")
        }

        if (event.key == Qt.Key_A) {
//            scene.move_camera(1);
            event.accepted = true;
            console.log("(a) Move camera left")
        }

        if (event.key == Qt.Key_D) {
//            scene.move_camera(1);
            event.accepted = true;
            console.log("(d) Move camera right")
        }

        if (event.key == Qt.Key_Space) {
//            scene.move_camera(1);
            event.accepted = true;
            console.log("(Space) Move camera ascend")
        }
    }

    ModelUnderlay {
        id: scene
    }

//    Rectangle {
//        id: rectangle
//        x: 40
//        y: 20
//        width: 120
//        height: 120
//        color: "red"
//
//        focus: true
//        Keys.onUpPressed: rectangle.y -= 10
//        Keys.onDownPressed: rectangle.y += 10
//        Keys.onLeftPressed: rectangle.x += 10
//        Keys.onRightPressed: rectangle.x -= 10
//    }

//    Timer {
//        interval: 20
//        running: true
//        repeat: true
//        onTriggered: {
//            triangle.theta = triangle.theta + 2.0
//            if (triangle.theta == 360.0) {
//                triangle.theta = 0.0
//            }
//        }
//    }

    Text {
        text: 'Simple 3D Editor By Kun'
        anchors {
            left: parent.left
            bottom: parent.bottom
            margins: 20
        }

        font.pointSize: 10
        color: 'white'
    }

    Button {
        id: add_cube_button
        text: 'Add Cube'
        anchors.top: parent.top
        anchors.right: parent.right

        mouse_area.onClicked: {
            scene.add_geometry(0)
        }
    }

    Button {
        id: delete_cube_button
        text: 'Delete Cube'
        anchors.top: add_cube_button.bottom
        anchors.right: parent.right

        mouse_area.onClicked: {
            scene.delete_geometry(0)
        }
    }

    Button {
        id: add_sphere_button
        text: 'Add Sphere'
        anchors.top: delete_cube_button.bottom
        anchors.right: parent.right

        mouse_area.onClicked: {
            scene.add_geometry(1)
        }
    }

    Button {
        id: delete_sphere_button
        text: 'Delete Sphere'
        anchors.top: add_sphere_button.bottom
        anchors.right: parent.right

        mouse_area.onClicked: {
            scene.delete_geometry(0)
        }
    }

    Button {
        id: stretch_x_button
        text: 'Stretch X'
        anchors.top: parent.top
        anchors.left: parent.left
    }

    Button {
        id: stretch_y_button
        text: 'Stretch Y'
        anchors.top: stretch_x_button.bottom
        anchors.left: parent.left
    }

    Button {
        id: stretch_z_button
        text: 'Stretch Z'
        anchors.top: stretch_y_button.bottom
        anchors.left: parent.left
    }

}