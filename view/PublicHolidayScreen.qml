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
        implicitWidth: parent.implicitWidth
        implicitHeight: parent.height
        anchors.top: pholiRect.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        topMargin: pholidayHorizontalHeader.height
        leftMargin: pholidayVerticalHeader.width

        clip: true
        columnSpacing: 1
        rowSpacing: 1
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
        }
    }
}
