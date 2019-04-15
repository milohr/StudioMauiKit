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
    menuButton.colorScheme.highlightColor: headBarFGColor
    searchButton.colorScheme.highlightColor: headBarFGColor
    headBarBGColor: "#484e78"
    headBarFGColor: "#fafafa"


    /***** PROPS *****/
    floatingBar: true
    footBarOverlap: true
    allowRiseContent: false
    altToolBars: false

    //property int currentView: views.start
    headBar.drawBorder: false
    headBar.middleContent: [
        Maui.ToolButton
        {
            onClicked: currentView = views.start
        }

    ]

    leftIcon.visible: false

    headBar.leftContent: [
        Maui.ToolButton
        {
            iconName: "application-menu"
            onClicked: slideView.visible = !slideView.visible
            iconColor: headBarFGColor
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
        colorScheme.backgroundColor: headBarBGColor
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

                    Maui.Button
                    {
                        id: buttonOpen
                        text: "Open"
                        height: iconSizes.big *1.3
                        width: height *2
                        //                        colorScheme.backgroundColor: hovered ? Qt.darker(headBarBGColor) : "transparent"
                        colorScheme.textColor: headBarFGColor
                        //                        colorScheme.borderColor: "#7079ba"

                        background: Rectangle {
                            border.color: "#7079ba"
                            border.width: 2
                            radius: 4
                            color: buttonOpen.hovered ? Qt.darker(headBarBGColor) : "transparent"
                        }


                    }

                    Maui.Button
                    {
                        id: buttonNew
                        text: "New"
                        //Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        //Layout.fillHeight: true
                        height: iconSizes.big *1.3
                        width: height *2
                        //                        colorScheme.backgroundColor: hovered ? Qt.darker(headBarBGColor) : "transparent"
                        colorScheme.textColor: headBarFGColor
                        //                        colorScheme.borderColor: "#7079ba"
                        background: Rectangle {
                            border.color: "#7079ba"
                            border.width: 2
                            radius: 4
                            color: buttonNew.hovered ? Qt.darker(headBarBGColor) : "transparent"
                        }

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
