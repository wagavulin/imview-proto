#!/usr/bin/env python

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
exit(app.exec())
