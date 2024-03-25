import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import io.qt.textproperties 1.0


Rectangle{
    id: loginRect
    color: "black"
    property string errorText: ""

    function checkDB(){
        var result = DbController.check_database_name(dbField.text)
        if (result){
            dbDisplay.db_valid = true
            dbDisplay.text = "Database: " + dbField.text + " exist"
        } else {
            dbDisplay.db_valid = false
            dbDisplay.text = "Database: no database found named " + dbField.text
            if( userField.text != "" && passField.text != "" && dbField.text != ""){
                createButton.visible = true
            }
        }
    }

    function checkUser(){
        if (userField.text != ""){
            uDisplay.u_valid = true
            uDisplay.text = "User: " + userField.text + " entered"
        }
    }

    function checkPass(){
        if (passField.text != ""){
            pwDisplay.pw_valid = true
            pwDisplay.text = "Password: password entered"
        }
    }

    ColumnLayout{
        anchors.centerIn: parent
        Row{
            Label{
                text: "Database: "
                color: "white"
                width:100
            }
            TextField{
                id: dbField
                width: 150
                color: "white"
                onTextChanged: checkDB()
            }
            Button{
                id: dbCheckButton
                text: "Check"
                width: 50
                highlighted: false
                onClicked: checkDB()
            }
        }
        Row{
            Label{
                width:100
                text: "Username: "
                color: "white"
            }
            TextField{
                id: userField
                width: 200
                color: "white"
                onTextChanged: checkUser()
            }
        }
        Row{
            Label{
                width:100
                text: "Password: "
                color: "white"
            }
            TextField{
                id: passField
                width: 150
                color: "white"
                echoMode: TextField.Password
                onTextChanged: checkPass()
            }
            Button{
                property bool show: false
                id: showPassButton
                text: show ?  "Hide" : "Show"
                width: 50
                highlighted: false
                onClicked: {
                    show = !show
                    passField.echoMode = show ? TextField.Normal : TextField.Password
                }
            }
        }
        Row{
            Button{
                id: loginButton
                text: "Login"
                width: 300
                highlighted: true
                onClicked: {
                    DbController.connect(dbField.text, userField.text, passField.text)
                }
            }
        }
        Row{
            Text{
                id: errorDisplay
                width: 300
                font.pixelSize: 12
                text: errorText
                color: "red"
            }
        }
        Row{
            Text{
                id: dbDisplay
                property bool db_valid: false
                width: 300
                font.pixelSize: 10
                text: "Database: invalid database name"
                color: db_valid ? "green" : "red"
            }
        }
        Row{
            Text{
                id: uDisplay
                property bool u_valid: false
                width: 300
                font.pixelSize: 10
                text: "User: enter Username"
                color: u_valid ? "green" : "red"
            }
        }
        Row{
            Text{
                id: pwDisplay
                property bool pw_valid: false
                width: 300
                font.pixelSize: 10
                text: "Password: enter Password"
                color: pw_valid ? "green" : "red"
            }
        }
        Row{
            Button{
                id: createButton
                text: "Create Database"
                width: 300
                highlighted: true
                visible: false
                onClicked: {
                    DbController.create_database(dbField.text, userField.text, passField.text)
                    visible = false
                }
            }
        }

    }

}