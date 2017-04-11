#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from mainwindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    LabelerMainWindow = MainWindow()
    LabelerMainWindow.setFocusPolicy(Qt.StrongFocus)
    LabelerMainWindow.show()
    sys.exit(app.exec_())
