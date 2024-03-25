import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.qt.textproperties 1.0

ApplicationWindow{
    visible: true
    width: 640
    height: 480
    title: "Work! Record! Report!"
    id: root

    menuBar: MenuBar {
        enabled: stackView.currentItem === mainScreen
        Menu {
            title: qsTr("&File")
            Action { text: qsTr("&New...") }
            Action { text: qsTr("&Open...") }
            MenuSeparator { }
            Action { text: qsTr("&Quit") }
        }
        Menu {
            title: qsTr("&Edit")
            Action { text: qsTr("Cu&t") }
            Action { text: qsTr("&Copy") }
            Action { text: qsTr("&Paste") }
        }
        Menu {
            title: qsTr("&Help")
            Action { text: qsTr("&About") }
        }
    }
    StackView {
        id: stackView
        initialItem: loginScreen
        anchors.fill: parent
        pushEnter: Transition {
            PropertyAnimation {
                property: "opacity";
                from: 0;
                to: 1;
                duration: 250
            }
        }
        popEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: 250
            }
        }
        popExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to: 0
                duration: 250
            }
        }

        LoginScreen {
            visible: false
            id: loginScreen
        }

        MainScreen {
            visible: false
            id: mainScreen
        }

    }
    Connections{
        target: DbController
        function onLoginSuccess(result){
            if (result){
                console.log("Login success")
                stackView.push(mainScreen)
            }
            else{
                loginScreen.errorText = "Login failed"
            }
        }
        function onLogoutSuccess(){
            stackView.pop()
        }
    }
}