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
        implicitWidth: parent.implicitWidth
        implicitHeight: parent.height
        anchors.top: sickRect.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        topMargin: sickdayHorizontalHeader.height
        leftMargin: sickdayVerticalHeader.width

        clip: true
        columnSpacing: 1
        rowSpacing: 1
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
        }
    }
}
