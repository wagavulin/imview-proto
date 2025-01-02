#!/usr/bin/env python

from PySide6 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("ImView")

        open_action = QtGui.QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open an image file")
        open_action.triggered.connect(self.open_file)

        exit_action = QtGui.QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

        vertical_layout = QtWidgets.QVBoxLayout()
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vertical_layout)
        self.setCentralWidget(central_widget)
        self.label = QtWidgets.QLabel("hello")
        vertical_layout.addWidget(self.label)

        self.statusBar().showMessage("Ready")
        self.show()

    def open_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image File", QtCore.QDir.homePath())
        if file_name:
            self.pixmap = QtGui.QPixmap(file_name)
            self.label.setPixmap(self.pixmap)

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = MainWindow()
    exit(app.exec())
