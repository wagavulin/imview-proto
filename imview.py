#!/usr/bin/env python

import glob
import os
from PySide6 import QtCore, QtGui, QtWidgets

class ImageDirectoryNavigator:
    def __init__(self, img_dir, initial_fname:str|None=None):
        self.img_dir = img_dir
        self.img_paths = sorted(list(glob.glob(os.path.join(img_dir, "*.JPG"))))
        if initial_fname:
            self.current_img_idx = self.img_paths.index(os.path.join(img_dir, initial_fname))
        else:
            self.current_img_idx = 0

    def get_current_img_path(self):
        return self.img_paths[self.current_img_idx]

    def get_next_img_path(self):
        self.current_img_idx = (self.current_img_idx + 1) % len(self.img_paths)
        return self.get_current_img_path()

    def get_prev_img_path(self):
        self.current_img_idx = (self.current_img_idx - 1) % len(self.img_paths)
        return self.get_current_img_path()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.image_directory_navigator:ImageDirectoryNavigator|None = None

        super(MainWindow, self).__init__(parent)
        self.setAcceptDrops(True)
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
        self.label = QtWidgets.QLabel("Open from File->Open or drag and drop an image file here")
        vertical_layout.addWidget(self.label)

        self.statusBar().showMessage("Ready")

        self.open_new_file("../sample-images/EOS100D-2024/IMG_5535.JPG")

        self.show()

    def open_new_file(self, img_path):
        img_dir, img_fname = os.path.split(img_path)
        self.image_directory_navigator = ImageDirectoryNavigator(img_dir, img_fname)
        self.load_and_show_image(self.image_directory_navigator.get_current_img_path())

    def open_file(self):
        img_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image File", QtCore.QDir.homePath())
        if img_path:
            self.load_and_show_image(img_path)

    def load_and_show_image(self, img_path):
        pixmap_orig = QtGui.QPixmap(img_path)
        self.pixmap = pixmap_orig.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.label.setPixmap(self.pixmap)
        img_fname = os.path.split(img_path)[1]
        self.setWindowTitle(f"ImView - {img_fname}")

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Right:
            self.image_directory_navigator.get_next_img_path()
            self.load_and_show_image(self.image_directory_navigator.get_current_img_path())
        elif e.key() == QtCore.Qt.Key_Left:
            self.image_directory_navigator.get_prev_img_path()
            self.load_and_show_image(self.image_directory_navigator.get_current_img_path())
        return super().keyPressEvent(e)

    def dragEnterEvent(self, e:QtGui.QDragEnterEvent):
        m:QtCore.QMimeData = e.mimeData()
        if m.hasText():
            e.accept()

    def dropEvent(self, e:QtGui.QDropEvent):
        img_path = e.mimeData().text()
        if img_path.startswith("file:///"):
            img_path = img_path[8:]
        if os.path.isfile(img_path):
            self.open_new_file(img_path)
        else:
            self.statusBar().showMessage(f"Invalid file: {img_path}")

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = MainWindow()
    exit(app.exec())
