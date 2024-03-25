// Dialog to create new topic
import QtQuick 2.0
import QtQuick.Controls
import QtQuick.Layouts
import io.qt.textproperties 1.0


Dialog{
    id: dialog
    title: "Create new topic"
    visible: true
    modal: true
    height: 400

    header: Text{
        text: "Create new topic"
        font.pixelSize: 20
    }
    footer: Text{
        text: "Click 'OK' to create a new topic or 'Cancel' to close the dialog."
        font.pixelSize: 12
    }
    TextField {
        id: topicName
        placeholderText: "Topic name"
    }
    Row{
        Button {
            text: "OK"
            onClicked: dialog.accept()
        }
        Button {
            text: "Cancel"
            onClicked: dialog.reject()
        }
    }
    onAccepted: {
        if(topicName.text === ""){
            DbController.addTopic(topicName.text)
        }
    }
}
