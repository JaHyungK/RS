import step2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys


class Win(QMainWindow, step2.Ui_MainWindow):

    def __init__(self):
        super(Win, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    app.exec_()