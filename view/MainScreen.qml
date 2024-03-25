import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import io.qt.textproperties 1.0




Rectangle {
    id: mainRect
    color: "black"

    Row{
        id: btnRow
        Button{
            text: "+ Topic"
            width: 200/3
            enabled: true
            onClicked: {
                console.log("Create Topic")
                var component = Qt.createComponent("CreateTopicDialog.qml")
                if (component.status === Component.Ready) {
                    var dialog = component.createObject(mainRect)
                    dialog.open()
                }else{
                    console.log("Error creating component" + component.errorString())
                }
            }
        }

        Button{
            text: "- Topic"
            enabled: false
            width:200/3
            onClicked: {
                DbController.removeTopic()
            }
        }

        Button{
            text: "Logout"
            width: 200/3
            onClicked: {
                DbController.disconnect()
            }
        }
    }

    ListView{
        id: topics
        width: 200
        anchors.top: btnRow.bottom
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        model: DbController.topicmodel
        delegate: Item {
            width: listView.width
            height: 50
            Text {
                text: model.name
                anchors.centerIn: parent
            }
        }
    }
    TableView{
        id: entries
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.left: topics.right
        height: parent.height*2/3
        model: DbController.entrymodel
        delegate: EntryDelegate{
            width: listView.width
            height: 50
        }
    }

    Rectangle{
        id: entry
        anchors.top: entries.bottom
        anchors.right: parent.right
        anchors.left: topics.right
        anchors.bottom: parent.bottom
        color: "darkgrey"
        ColumnLayout{
            Row{
                id: tagsRow
                Label{
                    id: dateLabel
                    text: "Date:"
                    width: 100
                }
                Text{
                    id: dateField
                    Layout.fillWidth: true
                    text: ""
                }
                Label{
                    id: startLabel
                    text: "Start:"
                    width: 100
                }
                Text{
                    id: startField
                    Layout.fillWidth: true
                    text: ""
                }
                Label{
                    id: endLabel
                    text: "End:"
                    width: 100
                }
                Text{
                    id: endField
                    Layout.fillWidth: true
                    text: ""
                }
            }
            Row{
                id: descriptionRow
                Label{
                    id: descriptionLabel
                    text: "Description:"
                    width: 100
                }
                TextArea{
                    id: textInput
                    height: 200
                    Layout.fillWidth: true
                    text: "Enter your text here"
                }
            }
            Row{
                Button{
                    id: startButton
                    text: "Start"
                    onClicked: {
                        DbController.startEntry()
                    }
                }
                Button{
                    id: stopButton
                    text: "Stop"
                    onClicked: {
                        DbController.endEntry()
                    }
                }
                Button{
                    id: discardButton
                    text: "Discard"
                    onClicked: {
                        DbController.discardEntry()
                    }
                }
            }
        }
    }
}