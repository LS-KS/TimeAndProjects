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
        enabled: stackView.currentItem != loginScreen
        Menu {
            title: qsTr("&File")
            Action {
                text: qsTr("&Preferences...")
                onTriggered: {
                    var component = Qt.createComponent("MetaDataDialog.qml")
                    if (component.status === Component.Ready) {
                        var dialog = component.createObject(root)
                        dialog.open()
                    }else{
                        console.log("Error creating component" + component.errorString())
                    }
                }
            }
            MenuSeparator { }
            Action {
                text: qsTr("&Show &All &Entries")
                onTriggered: {
                    DbController.updateEntryQuery("")
                }
            }
            Action{
                text: qsTr("&Goto &holidays")
                enabled: stackView.currentItem == mainScreen
                onTriggered: {
                    stackView.push(holidayScreen)
                }
            }
            Action{
                text: qsTr("&Goto &public Holidays")
                enabled: stackView.currentItem == mainScreen
                onTriggered: {
                    stackView.push(pholidayScreen)
                }
            }
            Action{
                text: qsTr("&Goto &sickdays")
                enabled: stackView.currentItem == mainScreen
                onTriggered: {
                    stackView.push(sickdayScreen)
                }
            }
            Action{
                text: qsTr("&Goto &Mainscreen ...")
                enabled: stackView.currentItem != mainScreen
                onTriggered:{
                    stackView.pop(mainScreen)
                }
            }
            MenuSeparator { }
            Action { text: qsTr("&Quit") }
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

        HolidayScreen{
            visible:false
            id: holidayScreen
        }

        PublicHolidayScreen{
            visible:false
            id: pholidayScreen
        }

        SickdayScreen{
            visible:false
            id: sickdayScreen
        }
        onCurrentItemChanged: {
            if(currentItem === holidayScreen){
                DbController.getUsedHolidays();
            }
            else if(currentItem === pholidayScreen){
                DbController.getPublicHolidayCount()
            }
            else if(currentItem === sickdayScreen){
                DbController.getSickDayCount()
            }
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
            stackView.pop(loginScreen)
        }
        function onDatabaseName(db){
            TopicModel.setDatabaseName(db)
            EntryModel.setDatabaseName(db)
        }
        function onTopicQueryChanged( query, db_name){
            TopicModel.setQuery(query, db_name)
        }
        function onEntryQueryChanged( query, db_name){
            EntryModel.setQuery(query, db_name)
        }
        function onHolidayQueryChanged(query, db_name){
            console.log("query of HolidayModel changed" + query +", " + db_name);
            HolidayModel.setQuery(query, db_name);
        }
        function onPublicHolidayQueryChanged(query, db_name){
            console.log("query of PublicHolidayModel changed" + query +", " + db_name);
            PublicHolidayModel.setQuery(query, db_name);
        }
        function onSickdayQueryChanged(query, db_name){
            console.log("query of SickdayModel changed" + query +", " + db_name);
            SickdayModel.setQuery(query, db_name);
        }
        function onNewYear(year){
            YearModel.addYear(year)
        }
        function onTopicDeleted(){
            DbController.updateEntryQuery("")
        }
    }
}
