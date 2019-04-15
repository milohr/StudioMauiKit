import QtQuick 2.2

Item
{
    width: root.width
    height: root.height

    SignalImage
    {
        id: signal1
        x:0
        source: "qrc:/assets/wave2.svg"
        antialiasing: true
        onClicked:
        {

        }
    }
}
