#!/usr/bin/env python

import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtUiTools import QUiLoader

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("ImView")

        self.loader = QUiLoader()
        self.window = self.loader.load("./mainwindow.ui", None)
        self.setCentralWidget(self.window)

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
exit(app.exec())
