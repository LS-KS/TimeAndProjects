import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import io.qt.textproperties 1.0
ScrollView {
    id: holidayRect
    ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
    ScrollBar.vertical.policy: ScrollBar.AlwaysOn

    property real holiday_entitlement: 0
    property real used_holidays: 0
    Connections{
        target: DbController
        function onUsedHolidays(days){
            holidayRect.used_holidays = parseFloat(days).toFixed(2)
        }
        function onHolidayEntitlement(days){
            holidayRect.holiday_entitlement = parseFloat(days).toFixed(2)
        }
    }
    Rectangle{
        id: holiRect
        border.color: "grey"
        color: "black"
        height: 30
        width: parent.width
        Label{
            text: "Holidays (" + used_holidays + "/" + holiday_entitlement+ " used)"
            color: "white"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
        }
    }
    HorizontalHeaderView{
        id: holidayHorizontalHeader
        syncView: holidayView
        clip: true
        anchors.top: holidayView.top
        anchors.left: holidayView.left
    }
    VerticalHeaderView{
        id: holidayVerticalHeader
        syncView: holidayView
        anchors.left: holidayView.left
        anchors.top: holidayView.top
    }
    TableView{
        id: holidayView
        model: HolidayModel
        implicitWidth: parent.implicitWidth
        implicitHeight: parent.height*2/3 - holidayEdit.height
        anchors.top: holiRect.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        topMargin: holidayHorizontalHeader.height
        leftMargin: holidayVerticalHeader.width
        boundsBehavior: Flickable.StopAtBounds
        clip: true
        columnSpacing: 1
        rowSpacing: 1
        property int selectedRow: 0
        property int selectedId: 0
        property bool selectionActive: false
        delegate: Rectangle{
            property bool selected: row === holidayView.selectedRow
            color: holidayView.selectionActive && selected? "green" : "black"
            implicitHeight: 30
            implicitWidth: column === 0 ? 20: 150
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
                    holidayView.selectedRow = row
                    holidayView.selectedId = HolidayModel.idOf(row)
                    holidayView.selectionActive = true
                    DbController.selectHolidayEntry(holidayView.selectedId)
                }
            }
        }

        Connections{
            target: DbController
            function onHolidayEntry(id, day, hours, year){
                console.log("id = "+id + "day: "+ day + "hours: " + hours + "year: "+ year)
                idField.text = id;
                dayField.text = day;
                hourField.text = hours;
                yearField.text = year;
            }
        }
    }
    Rectangle{
        id: holidayEdit
        anchors.top: holidayView.bottom
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
                    text: "Save"
                    onClicked: console.log("not implemented")
                }
                Button{
                    text: "Delete"
                    onClicked: console.log("not implemented")
                }
            }
        }
    }
}
