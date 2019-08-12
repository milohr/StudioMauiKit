import org.kde.kirigami 2.3 as Kirigami
import QtQuick 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.12

Kirigami.FormLayout {
   TextField {
      Kirigami.FormData.label: "Label:"
   }
   Kirigami.Separator {
       Kirigami.FormData.label: "Section Title"
       Kirigami.FormData.isSection: true
   }
   TextField {
      Kirigami.FormData.label: "Label:"
   }
   TextField {
   }
}
