import QtQuick 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.12
import org.kde.kirigami 2.0 as Kirigami
import org.kde.mauikit 1.0 as Maui

import "src/views/start"

Maui.ApplicationWindow
{
    id: root
    title: "Nebula"

    about.appDescription: qsTr("Nebula is a framework that works on desktops, Android and Plasma Mobile. Nebula lets you have the principals components for neuro apps and share them with external applications.")
    about.appName: qsTr("Nebula")
    //about.appVersion: qsTr("0.1")
    about.appIcon: "qrc:/brain(1).svg"

    /**** BRANDING COLORS ****/
//    menuButton.colorScheme.highlightColor: headBarFGColor
//    searchButton.colorScheme.highlightColor: headBarFGColor
//    headBarBGColor: "#484e78"
//    headBarFGColor: "#fafafa"


    /***** PROPS *****/

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
            close()
        }
        rejectButton.text: qsTr("Cancel")
        onRejected:
        {
            console.log("The creation of the project has been canceled")
            close()
        }
    }


    //property int currentView: views.start
    headBar.middleContent: [
        ToolButton
        {
            onClicked: currentView = views.start
        }

    ]

    leftIcon.visible: false

    headBar.leftContent: [
        ToolButton
        {
            visible: slideView.modal
            icon.name: "view-right-new"
            //iconName: "application-menu"
            onClicked: slideView.visible = !slideView.visible
            checkable: true
            checked: slideView.visible
            icon.color: headBarFGColor
        },
        ToolButton
        {
            icon.name: "go-parent-folder"
            onClicked:
            {
                fmDialog.filters = ["*.cnt"]  //Signals format allowed
                fmDialog.mode = fmDialog.modes.OPEN
                fmDialog.show(function(paths)
                {
                    console.log(paths)
                    loadFile.read(paths)
                    loadFile.update_path(paths) //Organizar bien el update
                })
            }
        },
        ToolButton
        {
            icon.name: "labplot-xy-interpolation-curve"
        },
        ToolButton
        {
            icon.name: "ps2pdf"
        }

    ]


    globalDrawer: Maui.GlobalDrawer
    {
        id: slideView
        width: Kirigami.Units.gridUnit * 15
        Button {
            text: "Button"
            onClicked: console.log("butos slideview")
        }

    }


    Maui.Page
    {
        id: page
        anchors.fill: parent
//        colorScheme.backgroundColor: headBarBGColor
        headBar.visible: false

        ColumnLayout
        {
            id: columnLayout
            spacing: 3
            anchors.centerIn: parent
            height: 200 * unit


            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignBottom

                Row
                {
                    anchors.centerIn: parent
                    spacing: space.medium

                    Button
                    {
                        id: buttonOpen
                        text: "Open"
                        height: iconSizes.big *1.3
                        width: height *2
                        onClicked:
                        {
                            console.log("Path from fm: " + fmDialog.initPath)
                            var dir = loadProject.settings_dir(fmDialog.initPath)
                            dir = dir.slice(0, dir.lastIndexOf('/'))
                            dir = [dir,'Nebula'].join('/').replace(/\/{2,}/, '/')

                            fmDialog.initPath = "file://" + dir // Because its local
                            console.log("Path from fm2: " + fmDialog.initPath)

                            fmDialog.filters = ["*.conf"]
                            fmDialog.singleSelection = true
                            fmDialog.mode = fmDialog.modes.OPEN
                            fmDialog.show(function(paths)
                            {
                                console.log(paths)
                                loadFile.set_project_name(paths)
                                var signal_path = loadProject.load(paths)
                                console.log(signal_path)
                                if (signal_path)
                                {
                                    console.log("Entro")
                                    loadFile.read(signal_path)
                                }
//                                var dir = loadProject.load(paths)
//                                console.log("desde qml2 "+dir)

//                                loadFile.read(paths)
//                                loadFile.update_path(paths)
                            })

                        }
                        //                        colorScheme.backgroundColor: hovered ? Qt.darker(headBarBGColor) : "transparent"
//                        colorScheme.textColor: headBarFGColor
                        //                        colorScheme.borderColor: "#7079ba"

//                        background: Rectangle {
//                            border.color: "#7079ba"
//                            border.width: 2
//                            radius: 4
//                            color: buttonOpen.hovered ? Qt.darker(headBarBGColor) : "transparent"
//                        }


                    }

                    Button
                    {
                        id: buttonNew
                        text: "New"
                        //Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        //Layout.fillHeight: true
                        height: iconSizes.big *1.3
                        width: height *2
                        onClicked:  mDialog.open()



                        //                        colorScheme.backgroundColor: hovered ? Qt.darker(headBarBGColor) : "transparent"
//                        colorScheme.textColor: headBarFGColor
                        //                        colorScheme.borderColor: "#7079ba"
//                        background: Rectangle {
//                            border.color: "#7079ba"
//                            border.width: 2
//                            radius: 4
//                            color: buttonNew.hovered ? Qt.darker(headBarBGColor) : "transparent"
//                        }

                    }

                }
            }

            Item {
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop

                Image
                {
                    id: nebulaIcon
                    source: "assets/brain(1).svg"
                    anchors.centerIn: parent
                    height: iconSizes.huge
                    width: height
                }

            }


        }



    }

}
