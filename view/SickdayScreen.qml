import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import io.qt.textproperties 1.0

ScrollView {
    id: sickView
    ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
    ScrollBar.vertical.policy: ScrollBar.AlwaysOn
    property int sickleavecount: 0
    Connections{
        target: DbController
        function onSickDayCount(days){
            sickView.sickleavecount = parseFloat(days).toFixed(2)
        }
    }

    Rectangle{
        id: sickRect
        border.color: "grey"
        color: "black"
        width: parent.width
        height: 30
        Label{
            text: "Sick leave (" + sickleavecount + ")"
            color: "white"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
        }
    }
    HorizontalHeaderView{
        id: sickdayHorizontalHeader
        syncView: sickdayView
        clip: true
        anchors.top: sickdayView.top
        anchors.left: sickdayView.left
    }
    VerticalHeaderView{
        id: sickdayVerticalHeader
        syncView: sickdayView
        anchors.left: sickdayView.left
        anchors.top: sickdayView.top
    }
    TableView{
        id: sickdayView
        model: SickdayModel
        implicitHeight: parent.height*2/3 - sickdayEdit.height
        anchors.top: sickRect.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        topMargin: sickdayHorizontalHeader.height
        leftMargin: sickdayVerticalHeader.width
        boundsBehavior: Flickable.StopAtBounds
        columnSpacing: 1
        rowSpacing: 1
        clip: true
        property int selectedRow: 0
        property int selectedId: 0
        property bool selectionActive: false
        delegate: Rectangle{
            property bool selected: row === sickdayView.selectedRow
            color: sickdayView.selectionActive && selected? "green" : "black"
            implicitHeight: 30
            implicitWidth: column === 0 ? 20 : 150
            Text{
                text: model.display
                anchors.fill: parent
                anchors.margins: 5
                color: column === 0? 'grey' : 'white'
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.WrapAnywhere
            }
            MouseArea{
                anchors.fill: parent
                onClicked: {
                    sickdayView.selectedRow = row;
                    sickdayView.selectedId = SickdayModel.idOf(row);
                    sickdayView.selectionActive = true;
                    DbController.selectSickdayEntry(sickdayView.selectedId);
                    result.visible = false;
                }
            }
        }
        Connections{
            target: DbController
            function onSickdayEntry(id, day, hours, year){
                //console.log("id = "+id + "day: "+ day + "hours: " + hours + "year: "+ year)
                idField.text = id;
                dayField.text = day;
                hourField.text = hours;
                yearField.text = year;
            }
        }
    }
    Rectangle{
        id: sickdayEdit
        anchors.top: sickdayView.bottom
        width: parent.width
        color: "black"
        ColumnLayout{
            anchors.fill:parent
            spacing: 10
            Row{
                spacing: 10
                Layout.fillWidth: true
                Label{
                    text: "Id: "
                    color: "white"
                }
                Text{
                    id: idField
                    text: ""
                    color: "white"
                }
                Label{
                    text: "Day: "
                    color: "white"
                }
                TextField{
                    id: dayField
                    text: ""
                    color: "white"
                }
                Label{
                    text: "Hours: "
                    color: "white"
                }
                TextField{
                    id: hourField
                    text:""
                    color: "white"
                }
                Label{
                    text: "Year"
                    color: "white"
                }
                TextField{
                    id: yearField
                    text: ""
                    color: "white"
                }
            }
            Row{
                Button{
                    id: saveButton
                    text: "Save"
                    enabled: sickdayView.selectionActive
                    onClicked: DbController.saveSickdayEntry(idField.text, dayField.text, hourField.text, yearField.text)
                }
                Button{
                    text: "Delete"
                    enabled: sickdayView.selectionActive
                    onClicked: {
                        DbController.deleteSickdayEntry(idField.text);
                    }
                }
                Button{
                    text: "New Entry"
                    enabled: true
                    onClicked: {
                        idField.text = -1
                        saveButton.enabled = true
                    }
                }
                Button{
                    text:"Today"
                    enabled: idField.text !== ""
                    onClicked: {
                        var date = new Date();
                        var year = date.getFullYear();
                        var month = (date.getMonth() + 1).toString().padStart(2, '0');
                        var day = date.getDate().toString().padStart(2, '0');
                        var hours_floatstring = DbController.getDailyHours();
                        dayField.text = year+"-"+month +"-" + day;
                        yearField.text = year;
                        hourField.text = hours_floatstring;
                    }
                }
            }
            Text {
                id: result
                text: qsTr("")
                visible: false
            }
            Connections{
                target: DbController
                function onSickdayEntrySaved(value){
                    if(value){
                        result.text = "Entry "+ idField.text + " successfully saved!";
                        result.color = "green";
                        idField.text = "";
                        dayField.text = "";
                        hourField.text = "";
                        yearField.text = "";
                    }else {
                        result.text = "Error while writing to DB!";
                        result.color = "red";
                    }
                    result.visible = true;
                    DbController.updateSickdayQuery();
                    DbController.getSickDayCount();
                    saveButton.enabled = sickdayView.selectionActive;
                }
                function onSickdayEntryDeleted(value){
                    if(value){
                        result.text = "Entry "+ idField.text + " successfully deleted!";
                        result.color = "green";
                        idField.text = "";
                        dayField.text = "";
                        hourField.text = "";
                        yearField.text = "";
                        sickdayView.selectionActive = false;
                    }else{
                        result.text = "Error while writing to DB!";
                        result.color = "red"
                    }
                    result.visible = true;
                    DbController.updateSickdayQuery();
                    DbController.getSickDayCount();
                }
                function onSickdayEntryDuplicate(id){
                    result.text = "Date " + dayField.text + "Already exists! Please update existing record with ID = "+ id + "!";
                    result.color = "yellow";
                    result.visible = true;
                }
                function onSickdayEntryNew(id){
                    result.text = "Successfully created new record with ID= " + id;
                    result.color = "green";
                    result.visible = true;
                }
            }
        }
    }
}
