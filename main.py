#!/usr/bin/env python3

from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QApplication()
    engine = QQmlApplicationEngine()

    context = engine.rootContext()
    engine.load("main.qml")

    if len(engine.rootObjects()) == 0:
        quit()
    app.exec_()
