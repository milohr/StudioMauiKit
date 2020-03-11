#!/usr/bin/env python3
# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)

import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtCore import QUrl, QResource
from PySide2.QtGui import QIcon

# from src.controlers.io import load_file
# from src.controlers.io import project_settings
# from src.controlers import process_actions


if __name__ == '__main__':

    QResource.registerResource("assets/assets.qrc");

    app = QApplication(sys.argv)
    app.setApplicationName("studio")
    app.setApplicationVersion("1.0.0")
    app.setApplicationDisplayName("Studio")
    app.setOrganizationName("Maui")
    app.setOrganizationDomain("org.maui.studio")
    app.setWindowIcon(QIcon("qrc:/brain(1).svg"))
    #QtQml.qmlRegisterType(LoginManager, 'LoginManager', 1, 0, 'LoginManager')
    engine = QQmlApplicationEngine()
    engine.load(QUrl("main.qml"))

    # Load project name
    # loadProject = project_settings.LoadProject()
    # Load Signal Path
    # loadFile = load_file.LoadFile()
    # Load process actions
    # loadProcess = process_actions.Process(engine)

    # engine.rootContext().setContextProperty("loadProject", loadProject)
    # engine.rootContext().setContextProperty("loadFile", loadFile)
    # engine.rootContext().setContextProperty("loadProcess", loadProcess)

    #settings = project_settings.ProjectSettings(loadProject, loadFile)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
