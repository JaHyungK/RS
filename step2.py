# -*- coding: utf-8 -*-

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(561, 546)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 25))

        self.horizontalLayout.addWidget(self.label)

        self.comboBox_drive = QComboBox(self.centralwidget)
        self.comboBox_drive.setObjectName(u"comboBox_drive")
        self.comboBox_drive.setMinimumSize(QSize(0, 25))

        self.horizontalLayout.addWidget(self.comboBox_drive)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_filter = QPushButton(self.centralwidget)
        self.pushButton_filter.setObjectName(u"pushButton_filter")
        self.pushButton_filter.setMinimumSize(QSize(100, 25))

        self.horizontalLayout.addWidget(self.pushButton_filter)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.label_status = QLabel(self.centralwidget)
        self.label_status.setObjectName(u"label_status")

        self.gridLayout.addWidget(self.label_status, 4, 0, 1, 1)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\ub4dc\ub77c\uc774\ube0c : ", None))
        self.pushButton_filter.setText(QCoreApplication.translate("MainWindow", u"\uac80\uc0c9", None))
        self.label_status.setText(QCoreApplication.translate("MainWindow", u"60\ucd08 \ud6c4\uc5d0 \uac31\uc2e0\ub429\ub2c8\ub2e4.", None))
    # retranslateUi
