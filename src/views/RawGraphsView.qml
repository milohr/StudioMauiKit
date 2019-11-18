import QtQuick 2.9
import QtQuick.Controls 2.3
import QtCharts 2.2
import org.kde.kirigami 2.7 as Kirigami
import org.kde.mauikit 1.0 as Maui


Maui.Page
{
    id: rawChart
    headBar.visible: true
    headBar.leftContent: ToolButton
    {
        icon.name: "draw-arrow-back"
        onClicked: stack.pop()

    }
    title: "Raw signals plot"

    ChartView
    {
        title: "Spline"
        anchors.fill: parent
        antialiasing: true

        SplineSeries
        {
            name: "SplineSeries"
            XYPoint { x: 0; y: 0.0 }
            XYPoint { x: 1.1; y: 3.2 }
            XYPoint { x: 1.9; y: 2.4 }
            XYPoint { x: 2.1; y: 2.1 }
            XYPoint { x: 2.9; y: 2.6 }
            XYPoint { x: 3.4; y: 2.3 }
            XYPoint { x: 4.1; y: 3.1 }
        }

    }
}
