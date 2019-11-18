import QtQuick 2.9
import QtQuick.Controls 2.3
import QtCharts 2.2
import org.kde.kirigami 2.7 as Kirigami
import org.kde.mauikit 1.0 as Maui


Maui.Page
{
    id: rawChart

    ChartView
    {
        id: chartview
        anchors.fill: parent
        antialiasing: true
        ValueAxis {
                    id: bscan0_xAxix
                    min: 0
                    max: 5
                }

                ValueAxis {
                    id: bscan0_yAxis
                    min: -50
                    max: 50
                }

//        PieSeries {
//            id: pieSeries

//        }


        Component.onCompleted:
        {
            //var serie = loadProcess.add_chart_bar(chartview)
            var serie2 = chartview.createSeries(ChartView.SeriesTypeScatter, "scatter series", bscan0_xAxix, bscan0_yAxis)
            console.log(serie2)
            loadProcess.fill_serie(serie2)
            //console.log(serie)
            //othersSlice = pieSeries.append([5, 10]);
            //pieSeries.find("Volkswagen").exploded = true;
            //serie.append("commands", [2, 2, 3])
        }
    }

}

