import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import io.qt.textproperties 1.0


Rectangle {
    id: mainRect
    color: 'black'

    TableModel {
        id: testmodel
        TableModelColumn { display: "id" }
        TableModelColumn { display: "topic" }

        rows: [
            {
                "id": "1",
                "topic": "black"
            },
            {
                "id": "2",
                "topic": "brown"
            },
            {
                "id": "3",
                "topic": "white"
            }
        ]
    }

    Row{
        id: btnRow
        ComboBox{
            id: yearbox
            width: 200/4
        }
        Button{
            text: "+ Topic"
            width: 200/4
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
            width:200/4
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

    TableView{
        id: topics
        width: 200
        anchors.top: btnRow.bottom
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        model: DbController.topicmodel
        //model: testmodel
        delegate: Rectangle {
            implicitHeight: 50
            implicitWidth: 100
            Text{
                text: model.display
                color: 'red'
            }
        }
    }
    HorizontalHeaderView {
        id: horizontalHeader
        anchors.left: entries.left
        anchors.top: parent.top
        syncView: entries
        clip: true
    }

    VerticalHeaderView {
        id: verticalHeader
        anchors.top: entries.top
        anchors.left: entries.left
        syncView: entries
        clip: true
    }
    TableView{
        id: entries
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.left: topics.right
        height: parent.height*2/3
        model: DbController.entrymodel
        clip: true
        columnSpacing: 1
        rowSpacing: 1

        delegate: Rectangle{
            Text{
                text: model.date
                anchors.left: parent.left
                anchors.leftMargin: 10
            }
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
