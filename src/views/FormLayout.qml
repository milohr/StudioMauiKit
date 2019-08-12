import QtQuick 2.9
import QtQuick.Controls 2.2
import org.kde.kirigami 2.6 as Kirigami
import QtQuick.Layouts 1.3

Kirigami.FormLayout {
    id: control
    maxHeight: isMobile ? parent.height * 0.95 : unit * 500
    maxWidth: unit * 700

   Kirigami.Separator {
       Kirigami.FormData.label: "Project Name"
       Kirigami.FormData.isSection: true
   }

   Item {
       Kirigami.FormData.isSection: true
   }

   TextField {
      Kirigami.FormData.label: "Name:"
   }

   TextField {
   }
}
