import QtQuick 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.12
import QtCharts 2.3
import org.kde.kirigami 2.0 as Kirigami
import org.kde.mauikit 1.0 as Maui
import "src"
import "src/views/start"
import "src/views"

Maui.ApplicationWindow
{
    id: root
    title: "Nebula"

    Maui.App.description: qsTr("Nebula is a end user app framework")

    //about.appDescription: qsTr("Nebula is a framework that works on desktops, Android and Plasma Mobile. Nebula lets you have the principals components for neuro apps and share them with external applications.")
    //about.appName: qsTr("Nebula")
    //about.appVersion: qsTr("0.1")
    Maui.App.iconName: "qrc:/brain(1).svg"

    property string mainPath: ""
    property int firstLoad: 0
    property int firstRealGraph: 0
    property bool secondChart: false

    /**** BRANDING COLORS ****/
//    menuButton.colorScheme.highlightColor: headBarFGColor
//    searchButton.colorScheme.highlightColor: headBarFGColor
//    headBarBGColor: "#484e78"
//    headBarFGColor: "#fafafa"


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
        //closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent | Popup.CloseOnPressOutside
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

    Component
    {
        id: firstPageComponent

        StackView
        {
            id: stack
            initialItem: view1

            Component
            {
                id: view1

                Maui.Page
                {
                    id: page
                    //anchors.fill: parent
                    //        colorScheme.backgroundColor: headBarBGColor
                    headBar.visible: false


                    ColumnLayout
                    {
                        id: columnLayout
                        spacing: 3
                        anchors.centerIn: parent
                        height: 200 * Maui.Style.unit


                        Item {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignBottom

                            Row
                            {
                                anchors.centerIn: parent
                                spacing: Maui.Style.space.medium

                                Button
                                {
                                    id: buttonOpen
                                    text: "Open"
                                    height: Maui.Style.iconSizes.big *1.3
                                    width: height *2
                                    onClicked:
                                    {
                                        console.log("Path from fm: " + fmDialog.currentPath)
                                        var dir = loadProject.settings_dir(fmDialog.currentPath)
                                        dir = dir.slice(0, dir.lastIndexOf('/'))
                                        dir = [dir,'Nebula'].join('/').replace(/\/{2,}/, '/')

                                        fmDialog.currentPath = "file://" + dir // Because its local
                                        console.log("Path from fm2: " + fmDialog.currentPath)
                                        fmDialog.settings.filters = ["*.conf"]
                                        fmDialog.singleSelection = true
                                        fmDialog.mode = fmDialog.modes.OPEN
                                        fmDialog.show(function(paths)
                                        {
                                            console.log(paths)
                                            loadFile.set_project_name(paths)
                                            var signal_path = loadProject.load(paths)
                                            mainPath = loadProject.get_name_project(paths)
                                            console.log("MAIN PATH: ", mainPath)
                                            console.log(signal_path)
                                            if (signal_path && signal_path !== "None")
                                            {
                                                console.log("Get in")
                                                loadFile.read(signal_path)
                                                fmDialog.close()
                                                stack.push(view2)
                                                //loadFile.raw_plot(signal_path)
                                                // page.SwipeView.view.incrementCurrentIndex()

                                            }
                                            else
                                            {
                                                console.log("This project dont have any file")
                                                fmDialog.close()
                                                mDialogPopup.open()

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
                                    height: Maui.Style.iconSizes.big *1.3
                                    width: height *2
                                    onClicked:
                                    {
                                        mDialog.open()
                                    }



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
                                height: Maui.Style.iconSizes.huge
                                width: height
                            }

                        }


                    }



                }
            }

            Component
            {
                id: view2

                RawGraphsView
                {
                    id: rawInitialChart

                    Component.onCompleted:
                    {
                        console.log("FINALIZO RAWGRAPHS")
                        console.log(mainPath)
                    }

                }

            }
        }



    }

    Component
    {
        id: secondPageComponent

        Rectangle
        {

            anchors.fill: parent
            color: "green"
            Layout.fillWidth: true
            Layout.fillHeight: true

        }
    }

    Component
    {
        id: barChartComponent

        BarChart
        {
            id: barChart
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
                fmDialog.settings.filters = ["*.cnt", "*.set"]  //Signals format allowed
                fmDialog.singleSelection = false
                fmDialog.mode = fmDialog.modes.OPEN
                fmDialog.show(function(paths)
                {
                    console.log(paths)
                    loadFile.read(paths)
                    loadFile.update_path(paths) //Organizar bien el update
                    fmDialog.close()
                    swipeView.currentIndex = 1
                    //page.SwipeView.view.incrementCurrentIndex()
                    if (firstLoad === 0)
                    {
                        loadFile.raw_plot(paths)
                        stack.push(view2);
                        firstLoad = 1
                    }
                })



            }
        },
        ToolButton
        {
            icon.name: "view-process-all-tree"
        },
        ToolButton
        {
            icon.name: "labplot-xy-interpolation-curve"
            onClicked:
            {

                if (firstRealGraph === 0 && firstLoad == 0)
                {
                    loadFile.raw_plot(firstRealGraph)
                }
            }
        },
        ToolButton
        {
            icon.name: "ps2pdf"
            onClicked:
            {
                var correct_pdf = loadProcess.generate_pdf(mainPath)
                if (correct_pdf)
                {
                    mDialogPopup.title = "Inform created"
                    mDialogPopup.message = ""
                    mDialogPopup.open()
                }
                else
                {
                    mDialogPopup.open()
                }
            }
        }

    ]


    sideBar: ActionsSideBar
    {
        // For modifications see src/views/ActionsSideBar.qml

    }


    SwipeView
    {
        id: swipeView
        anchors.fill: parent
        //Layout.fillHeight: true
        //Layout.fillWidth: true
        clip: true

        Loader
        {
            active: SwipeView.isCurrentItem || (item && item.depth > 1)
            sourceComponent: firstPageComponent
        }

        Loader
        {
            active: SwipeView.isCurrentItem
            sourceComponent:
            {

                secondPageComponent


            }
        }

        Loader
        {
            active: SwipeView.isCurrentItem
            sourceComponent:
            {
                if (secondChart){
                    barChartComponent
                }
            }
        }
    
    }


}
