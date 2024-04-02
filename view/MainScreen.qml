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
            width: topics.width/4
            model: YearModel
            textRole: "year"
            valueRole: "year"
            Component.onCompleted: {
                yearbox.currentIndex = 0
            }
        }
        Button{
            text: "+ Topic"
            width: topics.width/4
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
            width:topics.width/4
            onClicked: {
                DbController.removeTopic()
            }
        }

        Button{
            text: "Logout"
            width: topics.width/4
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
        property bool selectionActive: false
        width: parent.width/3
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
            color: selected && topics.selectionActive? "green" : "black"
            Text{
                id: deleText
                anchors.fill: parent
                anchors.margins: 5
                text: model.display
                color: column == 0? 'grey' : 'white'
                verticalAlignment: Text.AlignVCenter
            }
            MouseArea{
                anchors.fill: parent
                onClicked: {
                    topics.selectedRow = row
                    topics.selectionActive = true
                    console.log("selected topic: " + row + "(row)" + deleText.text )
                    DbController.updateEntryQuery(deleText.text)
                }
            }
            Connections{
                target: DbController
                function onTopicStandardQuery(value){
                    if(value) {
                        topics.selectionActive = false
                    }
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
        anchors.left: topics.right
        syncView: entries
        clip: true
    }
    TableView{
        id: entries
        anchors.top: horizontalHeader.bottom
        anchors.right: parent.right
        anchors.left: verticalHeader.right
        height: parent.height*2/3
        model: EntryModel
        clip: true
        columnSpacing: 1
        rowSpacing: 1

        delegate: Rectangle{
            id: entrydDelegateRect
            implicitHeight: 30
            implicitWidth:  100
            color: "black"
            Text{
                id: entrydDelegateText
                anchors.fill: parent
                anchors.margins: 5
                text: model.display
                color: 'white'
                verticalAlignment: Text.AlignVCenter
            }

        }
    }

    Rectangle{
        id: entry
        property bool entryActive: false
        anchors.top: entries.bottom
        anchors.right: parent.right
        anchors.left: topics.right
        anchors.bottom: parent.bottom
        color: "black"
        border.color: entryActive ? "green" : "black"
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
                    id: newButton
                    text: "New Entry with actual Topic"
                    onClicked: {
                        entry.entryActive = true
                    }
                }
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
                        entry.entryActive = false
                        DbController.discardEntry()
                    }
                }
            }
        }
    }
}
