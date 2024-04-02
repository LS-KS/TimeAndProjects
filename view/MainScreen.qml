import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.qt.textproperties 1.0

Rectangle {
    id: mainRect
    color: 'black'

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
    HorizontalHeaderView {
            id: topicHeader
            anchors.left: parent.left
            anchors.top: btnRow.bottom
            syncView: topics
            clip: true
    }
    TableView{
        id: topics
        property int selectedRow
        width: 200
        anchors.top: topicHeader.bottom
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        model: TopicModel
        selectionBehavior: TableView.SelectRows
        columnWidthProvider: function(column){
            return column === 0 ? 20 : 100
        }
        delegate: Rectangle {
            id: deleRect
            property bool selected: row == topics.selectedRow
            implicitHeight: 30
            implicitWidth:  100
            color: selected? "green" : "black"
            Text{
                id: deleText
                anchors.fill: parent
                anchors.margins: 5
                text: model.display + row
                color: column == 0? 'grey' : 'white'
                verticalAlignment: Text.AlignVCenter
            }
            MouseArea{
                anchors.fill: parent
                onClicked: {
                    topics.selectedRow = row
                    console.log("selected topic: " + row + "(row)" + deleText.text )
                }
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
