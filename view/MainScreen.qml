import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.qt.textproperties 1.0

Rectangle {
    id: mainRect
    color: 'black'
    property string username: ""
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
            onCurrentValueChanged:{
                DbController.setYear(currentValue)
                //console.log(currentValue)
            }
        }
        Button{
            text: "+ Topic"
            width: topics.width/4
            enabled: true
            onClicked: {
                //console.log("Create Topic")
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
            id: removeTopicButton
            enabled: false
            width:topics.width/4
            onClicked: {
                DbController.removeTopic(topics.topicID)
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
        property int selectedRow :0
        property int topicID : 0
        property string topic: ""
        property bool selectionActive: false
        property int maxwidth: 300
        width: parent.width/3 >= maxwidth ? maxwidth : parent.width/3
        anchors.top: topicHeader.bottom
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        model: TopicModel
        selectionBehavior: TableView.SelectRows
        columnWidthProvider: function(column){
            return column === 0 ? 20 : width - 20
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
                wrapMode: Text.WrapAnywhere
            }
            MouseArea{
                anchors.fill: parent
                onClicked: {
                    topics.selectedRow = row
                    topics.topicID = TopicModel.idOf(row)
                    topics.topic = TopicModel.topicOf(row)
                    topics.selectionActive = true
                    //console.log("selected topic: " + row + "(row)" + deleText.text )
                    DbController.updateEntryQuery(topics.topic)
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
        height: parent.height - form.heightsum
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
                wrapMode: Text.WordWrap
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
        radius: 3
        border.color: entryActive ? "green" : "black"
        ColumnLayout{
            anchors.fill: parent
            anchors.margins: 15
            spacing: 15
            id: form
            property int heightsum: infoRow.implicitHeight + tagsRow.implicitHeight + descriptionRow.implicitHeight + entryBtnRow.implicitHeight + 5*spacing + 30
            Row{
                id: infoRow
                Layout.fillWidth: false
                spacing: 15
                Label{
                    text: "Topic:"
                    width: 50
                }
                Text{
                    id: topicIdField
                    text: ""
                    color: "white"
                }
                Text{
                    id: topicNameField
                    text: ""
                    color: "white"
                }
                Label{
                    text: "Record:"
                    width: 50
                }
                Text{
                    id: recordIDField
                    text: ""
                    color: "white"
                }
                Label{
                    text: "Last saved:"
                    width: 50
                }
                Text{
                    id: savedAt
                    text: ""
                    color: "white"
                }
            }
            Row{
                id: tagsRow
                Layout.fillWidth: true
                spacing: 15
                Label{
                    id: dateLabel
                    text: "Date:"
                }
                TextField{
                    id: dateField
                    text: ""
                    color: "white"
                }
                Label{
                    id: startLabel
                    text: "Start:"
                }
                TextField{
                    id: startField
                    Layout.fillWidth: true
                    text: ""
                    color: "white"
                }
                Label{
                    id: endLabel
                    text: "End:"
                }
                TextField{
                    id: endField
                    Layout.fillWidth: true
                    color: "white"
                    text: ""
                    onTextChanged:{
                        updateDuration()
                    }
                }
                Label{
                    id: durationLabel
                    text: "Duration"
                }
                Text{
                    property var defaultSize : 12
                    id: durationField
                    Layout.fillWidth: true
                    text: ""
                    color: "white"
                    font.pointSize: timer.running ? 20 : defaultSize
                    Component.onCompleted: {
                        defaultSize = font.pointSize
                    }
                }
            }
            Row{
                id: descriptionRow
                Layout.fillWidth: true

                Label{
                    id: descriptionLabel
                    text: "Description:"
                }
                TextArea{
                    id: textInput
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    placeholderText: "Enter your text here"
                    background: Rectangle {
                        implicitWidth: form.width -10 - descriptionLabel.width
                        color: "black"
                        border.color: entry.entryActive ? "#21be2b" : "transparent"
                    }
                }
            }
            Row{
                id: entryBtnRow
                Layout.fillWidth: true
                Button{
                    id: newButton
                    text: "New Entry with actual topic"
                    enabled: !timer.running && topics.selectionActive
                    onClicked: startTimer()
                }
                Button{
                    id: stopButton
                    text: "Stop"
                    enabled: timer.running
                    onClicked: endTimer()
                }
                Button{
                    id: discardButton
                    text: "Discard"
                    enabled: timer.running
                    onClicked: {
                        entry.entryActive = false
                        timer.running = false
                        startField.text = ""
                        endField.text = ""
                        durationField.text = ""
                        textInput.text =""
                        dateField.text = ""
                        topicIdField.text = ""
                        topicNameField.text = ""
                        recordIDField.text = ""
                        savedAt.text = ""
                    }
                }
                Button{
                    id: saveButton
                    text: "Save"
                    enabled: startField.text!= "" && textInput.text!="" && durationField.text !=""
                    onClicked: {
                        endTimer()
                        entry.entryActive = false
                        DbController.saveEntry(
                            recordIDField.text === savedAt.text,
                            recordIDField.text,
                            mainRect.username,
                            topicNameField.text,
                            textInput.text,
                            yearbox.currentValue,
                            dateField.text,
                            startField.text,
                            endField.text,
                            durationField.text
                            )
                    }
                }
            }
        }
    }
    Timer {
        id: timer
        interval: 500
        running: false
        repeat: true
        onTriggered: {
            updateDuration();
        }
    }
    function updateDuration() {
        var startTimeString = startField.text;
        var startTimeParts = startTimeString.split(':');
        var startTime = new Date();
        startTime.setHours(  parseInt(startTimeParts[0]));
        startTime.setMinutes(parseInt(startTimeParts[1]));
        startTime.setSeconds(parseInt(startTimeParts[2]));

        var currentTime = new Date();

        if (endField.text ===""){
            var diff = new Date(currentTime - startTime);
        } else{
            var endTimeString = endField.text;
            var endTimeParts = endTimeString.split(':');
            var endTime = new Date();
            endTime.setHours(  parseInt(endTimeParts[0]));
            endTime.setMinutes(parseInt(endTimeParts[1]));
            endTime.setSeconds(parseInt(endTimeParts[2]));
            var diff = new Date(endTime - startTime);
        }
        durationField.text = diff.toISOString().substr(11, 8);
    }
    function startTimer(){
        startField.text = new Date().toLocaleTimeString().replace(/\.\d+/, '')
        dateField.text = new Date().toLocaleDateString()
        topicIdField.text = topics.topicID
        topicNameField.text = topics.topic
        timer.running = true
        entry.entryActive = true
    }
    function endTimer(){
        timer.running = false
        endField.text = new Date().toLocaleTimeString().replace(/\.\d+/, '')
    }
    Connections{
        target: EntryModel
        function onEmptyTopic(value){
            removeTopicButton.enabled = value
        }
    }
    Connections{
        target: DbController
        function onUsername(username){
            mainRect.username = username
        }
    }
}
