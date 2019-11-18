import QtQuick 2.9
import QtQuick.Controls 2.3
import QtCharts 2.2
import org.kde.kirigami 2.7 as Kirigami
import org.kde.mauikit 1.0 as Maui


Maui.ActionSideBar
{
    id: slideView
    preferredWidth: Kirigami.Units.gridUnit * 10
    collapsible: true
    collapsed: !root.isWide

    Action {
        text: "Button"
        onTriggered: console.log("button slideview")
        icon.name: "anchor"
    }
    Action {
        id: action1
        text: "Button2"
        onTriggered:
        {
            console.log("button2 slideview")
            console.log(mainPath)
            var result_process1 = loadProcess.my_process_1(mainPath)
            var process1 = loadProcess.process_settings(mainPath, action1.text)
            console.log(result_process1)
            secondChart = true
            swipeView.currentIndex = 2;
        }
        icon.name: "anchor"
    }

    Action {
        id: action2
        text: "Button3"
        onTriggered: console.log("button3 slideview")
        icon.name: "anchor"
    }

}
