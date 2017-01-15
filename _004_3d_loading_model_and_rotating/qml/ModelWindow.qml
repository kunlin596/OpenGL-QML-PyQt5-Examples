import QtQuick 2.0
import OpenGLUnderQml 1.0
import QtGraphicalEffects 1.0

Item {
    width: 640
    height: 480

    focus: true
    Keys.onPressed: {
        if (event.key == Qt.Key_W) {
            scene.move_camera(0);
            event.accepted = true;
//            console.log("(w) Move camera forward")
        }
        if (event.key == Qt.Key_S) {
            scene.move_camera(1);
            event.accepted = true;
//            console.log("(s) Move camera backward")
        }

        if (event.key == Qt.Key_A) {
            scene.move_camera(2);
            event.accepted = true;
//            console.log("(a) Move camera left")
        }

        if (event.key == Qt.Key_D) {
            scene.move_camera(3);
            event.accepted = true;
//            console.log("(d) Move camera right")
        }

        if (event.key == Qt.Key_O) {
            scene.move_camera(4);
            event.accepted = true;
//            console.log("(Space) Move camera ascend")
        }

        if (event.key == Qt.Key_P) {
            scene.move_camera(5);
            event.accepted = true;
//            console.log("(Space) Move camera ascend")
        }
    }

//    MouseArea {
//        onPositionChanged: {
//            console.log(mouse.x, mouse.y)
//            console.log('OK')
//        }
//    }

    ModelUnderlay {
        id: scene
    }

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
            scene.delete_geometry(1)
        }
    }

    Button {
        id: stretch_x_button
        text: 'Stretch X'
        anchors.top: parent.top
        anchors.left: parent.left
        mouse_area.onClicked: {
            scene.stretch_x()
        }
    }

    Button {
        id: shrink_x_button
        text: 'Shrink X'
        anchors.top: parent.top
        anchors.left: stretch_x_button.right
        mouse_area.onClicked: {
            scene.shrink_x()
        }
    }

    Button {
        id: stretch_y_button
        text: 'Stretch Y'
        anchors.top: stretch_x_button.bottom
        anchors.left: parent.left
        mouse_area.onClicked: {
            scene.stretch_y()
        }
    }

    Button {
        id: shrink_y_button
        text: 'Shrink Y'
        anchors.top: shrink_x_button.bottom
        anchors.left: stretch_y_button.right
        mouse_area.onClicked: {
            scene.shrink_y()
        }
    }

    Button {
        id: stretch_z_button
        text: 'Stretch Z'
        anchors.top: stretch_y_button.bottom
        anchors.left: parent.left
        mouse_area.onClicked: {
            scene.stretch_z()
        }
    }

    Button {
        id: shrink_z_button
        text: 'Shrink Z'
        anchors.top: shrink_y_button.bottom
        anchors.left: stretch_z_button.right
        mouse_area.onClicked: {
            scene.shrink_z()
        }
    }

    Button {
        id: bigger_button
        text: 'Bigger'
        anchors.top: change_random_sphere_color.bottom
        anchors.left: parent.left
        mouse_area.onClicked: {
            scene.bigger_objects()
        }
    }

    Button {
        id: smaller_button
        text: 'Smaller'
        anchors.top: bigger_button.bottom
        anchors.left: parent.left
        mouse_area.onClicked: {
            scene.smaller_objects()
        }
    }


    Button {
        id: change_random_cube_color
        text:'Cube Color'
        anchors.top: stretch_z_button.bottom
        anchors.left: parent.left
        mouse_area.onClicked: {
            scene.change_random_cube_color()
        }
    }

    Button {
        id: change_random_sphere_color
        text:'Sphere Color'
        anchors.top: change_random_cube_color.bottom
        anchors.left: parent.left
        mouse_area.onClicked: {
            scene.change_random_sphere_color()
        }
    }


}