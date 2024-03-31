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

    header: Text{
        text: "Create new topic"
        font.pixelSize: 20
    }
    contentItem: TextField {
                    id: topicName
                    placeholderText: "Topic name"
                    KeyNavigation.tab: topicOkButton
                    Keys.onReturnPressed: dialog.accept() // Enter key
                    Keys.onEnterPressed: dialog.accept() // Numpad enter key
                    Keys.onEscapePressed: dialog.reject() // Escape
                }
    footer: Row{
                Button {
                    id: topicOkButton
                    text: "OK"
                    onClicked: dialog.accept()
                    KeyNavigation.tab: topicCancelButton
                }
                Button {
                    id: topicCancelButton
                    text: "Cancel"
                    onClicked: dialog.reject()
                    KeyNavigation.tab: topicName
                }
            }
    onAccepted: {
        if(topicName.text === ""){
            DbController.addTopic(topicName.text)
        }
    }
}
