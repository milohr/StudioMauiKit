import QtQuick 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.12
import QtCharts 2.3
import org.kde.kirigami 2.7 as Kirigami
import org.kde.mauikit 1.0 as Maui
import "src"
import "src/views/start"
import "src/views"

Maui.ApplicationWindow
{
    id: root
    title: "Nebula"

    Maui.App.description: qsTr("Nebula is a end user app framework")
    Maui.App.iconName: "qrc:/brain(1).svg"

    property string mainPath: ""
    property int firstLoad: 0
    property int firstRealGraph: 0
    property bool secondChart: false

    /**** BRANDING COLORS ****/


    /***** PROPS *****/


    Timer {
        id: popupClose
        interval: 2000
        onTriggered: mDialogPopup.close()
    }

    Maui.Dialog
    {
        id: mDialogPopup
        title: "Warning"
        message: "Sorry, But this project has no file available, try again"
        defaultButtons: false
        onOpened: popupClose.start()
    }

    Maui.FileDialog
    {
        id: fmDialog
    }

    Maui.Dialog
    {
        id: mDialog
        title: "Project name"
        message: ""
        //confirmationDialog: true
        entryField: true
        acceptButton.text: qsTr("Create")
        onAccepted:
        {
            console.log(textEntry.text)
            console.log(loadProject.create(textEntry.text))
            loadProject.create(textEntry.text)
            loadFile.assign_project(textEntry.text)
            mainPath = textEntry.text
            close()
            firstLoad = 0
        }
        rejectButton.text: qsTr("Cancel")
        onRejected:
        {
            console.log("The creation of the project has been canceled")
            close()
        }
    }



    headBar.middleContent: [
        ToolButton
        {
        icon.name: "love"
            onClicked: currentView = views.start
        }

    ]



    sideBar: ActionsSideBar
    {
        // For modifications see src/views/ActionsSideBar.qml

    }


    Maui.Page
    {
        id: swipeView
        anchors.fill: parent

        Maui.ListBrowser
        {
        anchors.fill: parent

        model: 30

        delegate: Maui.ListBrowserDelegate
        {
          height: 80
          width: parent.width
          padding: 10
          
          Kirigami.Theme.backgroundColor: "red"



        }

        }

    }


}
