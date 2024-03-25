import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


RowLayout{
    property bool open: true
    Layout.fillWidth: true
    Layout.preferredHeight: 50
    spacing: 5
    Rectangle{
        Layout.preferredWidth: 50
        Layout.preferredHeight: 50
        color: open? "red": "green"
    }
    Text{
        text: model.id
        Layout.preferredWidth: 50
    }
    Text{
        text: model.start
        Layout.fillWidth: true
    }
    Text{
        text: model.end
        Layout.fillWidth: true
    }
    Text{
        text: model.duration
        Layout.fillWidth: true
    }
    Text{
        text: model.description
        Layout.fillWidth: true
    }
}