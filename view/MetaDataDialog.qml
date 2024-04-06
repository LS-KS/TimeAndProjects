import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts

import io.qt.textproperties 1.0

Dialog {
    header: Label{
        text: "Metadata for Company and Employee"
        font.pointSize: 20
    }

    contentItem: Column{
        GridLayout{
            id: companyGrid
            columns: 2
            Layout.fillWidth: true
            Label{
                text: "Company Name"
            }
            TextField{
                id: companyNamefield
                text: ""
            }
            Label{
                text: "Street"
            }
            TextField{
                id: companyStreetfield
                text: ""
            }
            Label{
                text: "Zip"
            }
            TextField{
                id: companyZipfield
                text: ""
            }
            Label{
                text: "City"
            }
            TextField{
                id: companyCityfield
                text: ""
            }
            Label{
                text: "Email"
            }
            TextField{
                id: companyEmailfield
                text: ""
            }
            Label{
                text: "Company Phone"
            }
            TextField{
                id: companyPhonefield
                text: ""
            }
        }
        Rectangle{
            height: 5
            width: parent.width
            color: "green"
        }
        GridLayout{
            id: employeeGrid
            columns: 2
            Layout.fillWidth: true
            Label{
                text: "Employee Name"
            }
            TextField{
                id: employeeNamefield
                text: ""
            }
            Label{
                text: "Street"
            }
            TextField{
                id: employeeStreetfield
                text: ""
            }
            Label{
                text: "Zip"
            }
            TextField{
                id: employeeZipfield
                text: ""
            }
            Label{
                text: "City"
            }
            TextField{
                id: employeeCityfield
                text: ""
            }
            Label{
                text: "Email"
            }
            TextField{
                id: employeeEmailfield
                text: ""
            }
            Label{
                text: "Phone"
            }
            TextField{
                id: employeePhonefield
                text: ""
            }
            Label{
                text: "Personal ID"
            }
            TextField{
                id: employeeIdfield
                text: ""
            }
            Label{
                text: "Holidays (days)"
            }
            TextField{
                id: holidayEntitlementfield
                text: ""
            }
            Label{
                text: "Weekly hours"
            }
            TextField{
                id: weeklyHoursfield
                text: ""
            }
            Label{
                text: "Daily hours"
            }
            TextField{
                id: dailyHoursfield
                text: ""
            }
        }
    }
    footer: DialogButtonBox{
        standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel
        onAccepted: DbController.save_metadata(
                        companyNamefield.text,
                        companyStreetfield.text,
                        companyZipfield.text,
                        companyCityfield.text,
                        companyEmailfield.text,
                        companyPhonefield.text,

                        employeeNamefield.text,
                        employeeStreetfield.text,
                        employeeZipfield.text,
                        employeeCityfield.text,
                        employeeIdfield.text,
                        employeeEmailfield.text,
                        employeePhonefield.text,
                        holidayEntitlementfield.text,
                        weeklyHoursfield.text,
                        dailyHoursfield.text
                        )
        onRejected: console.log("Cancel clicked")
    }
    Component.onCompleted: {
        DbController.load_metadata()
    }
    Connections{
        target: DbController
        function onMetadata(
            companyName,
            companyStreet,
            companyCity,
            companyZip,
            companyEmail,
            companyPhone,
            employeeName,
            employeeStreet,
            employeeCity,
            employeeZip,
            employeeEmail,
            employeePhone,
            employeeId,
            holidays,
            weeklyHours,
            dailyHours,
            ){
            companyNamefield.text = companyName;
            companyStreetfield.text = companyStreet;
            companyZipfield.text = companyZip;
            companyCityfield.text = companyCity;
            companyEmailfield.text = companyEmail;
            companyPhonefield.text = companyPhone;

            employeeNamefield.text = employeeName;
            employeeStreetfield.text = employeeStreet;
            employeeZipfield.text = employeeZip;
            employeeCityfield.text = employeeCity;
            employeeIdfield.text = employeeId;
            employeeEmailfield.text = employeeEmail;
            employeePhonefield.text = employeePhone;
            holidayEntitlementfield.text = holidays;
            weeklyHoursfield.text = weeklyHours;
            dailyHoursfield.text = dailyHours;
        }
    }
}
