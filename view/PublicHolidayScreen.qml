import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.qt.textproperties 1.0

ScrollView {
    id: pholiView
    property int public_holidaycount: 0
    Connections{
        target: DbController
        function onPublicHolidayCount(days){
            pholiView.public_holidaycount = parseFloat(days).toFixed(2)
        }
    }
    ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
    ScrollBar.vertical.policy: ScrollBar.AlwaysOn
    Rectangle{
        id: pholiRect
        border.color: "grey"
        color: "black"
        height: 30
        width: parent.width
        Label{
            text: "Public holidays (" + public_holidaycount + ")"
            color: "white"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
        }
    }
    HorizontalHeaderView{
        id: pholidayHorizontalHeader
        syncView: pholidayView
        clip: true
        anchors.top: pholidayView.top
        anchors.left: pholidayView.left
    }
    VerticalHeaderView{
        id: pholidayVerticalHeader
        syncView: pholidayView
        anchors.left: pholidayView.left
        anchors.top: pholidayView.top
    }
    TableView{
        id: pholidayView
        model: PublicHolidayModel
        implicitHeight: parent.height*2/3 - pholidayEdit.height
        anchors.top: pholiRect.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        topMargin: pholidayHorizontalHeader.height
        leftMargin: pholidayVerticalHeader.width
        boundsBehavior: Flickable.StopAtBounds
        columnSpacing: 1
        rowSpacing: 1
        clip: true
        property int selectedRow: 0
        property int selectedId: 0
        property bool selectionActive: false
        delegate: Rectangle{
            property bool selected: row === pholidayView.selectedRow
            color: pholidayView.selectionActive && selected? "green" : "black"
            implicitHeight: 30
            implicitWidth: column === 0 ? 20 : column ===3 ? 300 : 150
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
                    pholidayView.selectedRow = row;
                    pholidayView.selectedId = PublicHolidayModel.idOf(row);
                    //console.log("selected Row - ID: " + pholidayView.selectedId)
                    pholidayView.selectionActive = true;
                    DbController.selectPublicHolidayEntry(pholidayView.selectedId);
                    result.visible = false;
                }
            }
        }
        Connections{
            target: DbController
            function onPublicHolidayEntry(id, day, description, hours, year){
                //console.log("id = "+id + "day: "+ day + "description: " + description + "hours: " + hours + "year: "+ year)
                idField.text = id;
                dayField.text = day;
                descriptionField.text = description;
                hourField.text = hours;
                yearField.text = year;
            }
        }
    }
    Rectangle{
        id: pholidayEdit
        anchors.top: pholidayView.bottom
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
                Label{
                    text: "Description: "
                    color: "white"
                }
                TextField{
                    id: descriptionField
                    Layout.fillWidth: true
                    color: "white"
                    text: ""
                }
            }
            Row{
                Button{
                    id: saveButton
                    text: "Save"
                    enabled: pholidayView.selectionActive
                    onClicked: {
                        DbController.savePublicHolidayEntry(idField.text, dayField.text, descriptionField.text, hourField.text, yearField.text);
                        DbController.getPublicHolidayCount();
                    }
                }
                Button{
                    text: "Delete"
                    enabled: pholidayView.selectionActive
                    onClicked: {
                        DbController.deletePublicHolidayEntry(idField.text);
                        DbController.getPublicHolidayCount();
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
                function onPublicHolidayEntrySaved(value){
                    if(value){
                        result.text = "Entry "+ idField.text + " successfully saved!";
                        result.color = "green";
                        idField.text = "";
                        dayField.text = "";
                        hourField.text = "";
                        yearField.text = "";
                        descriptionField.text = "";
                    }else {
                        result.text = "Error while writing to DB!";
                        result.color = "red";
                    }
                    result.visible = true;
                    DbController.updatePublicHolidayQuery();
                    saveButton.enabled = pholidayView.selectionActive;
                }
                function onPublicHolidayEntryDeleted(value){
                    if(value){
                        result.text = "Entry "+ idField.text + " successfully deleted!";
                        result.color = "green";
                        idField.text = "";
                        dayField.text = "";
                        hourField.text = "";
                        yearField.text = "";
                        descriptionField.text = "";
                        pholidayView.selectionActive = false;
                    }else{
                        result.text = "Error while writing to DB!";
                        result.color = "red"
                    }
                    result.visible = true;
                    DbController.updatePublicHolidayQuery();
                }
                function onPublicHolidayEntryDuplicate(id){
                    result.text = "Date " + dayField.text + "Already exists! Please update existing record with ID = "+ id + "!";
                    result.color = "yellow";
                    result.visible = true;
                }
                function onPublicHolidayEntryNew(id){
                    result.text = "Successfully created new record with ID= " + id;
                    result.color = "green";
                    result.visible = true;
                }
            }
        }
    }
}
