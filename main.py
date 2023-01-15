import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2 import QtGui
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from PySide2.QtCore import *

# GUI FILE
from app_modules import *
# SINGLE APP
from core.app import QtSingleApplication


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ########################################################################
        # 시스템 트레이 기반 윈도우 기능
        ########################################################################
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("RS")
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        # 트레이 메뉴
        show_action = QAction("윈도우 실행", self)
        quit_action = QAction("프로그램 종료", self)
        hide_action = QAction("최소화", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.icon_activated)

        print('System: ' + platform.system())
        print('Version: ' +platform.release())

        UIFunctions.removeTitleBar(True)

        self.setWindowTitle('RS')
        UIFunctions.labelTitle(self, 'RS')
        UIFunctions.labelDescription(self, '')

        # 윈도우 기본 사이즈
        startSize = QSize(1800, 920)
        self.resize(startSize)
        self.setMinimumSize(startSize)

        self.ui.stackedWidget.setMinimumWidth(20)

        UIFunctions.userIcon(self, "RS", "", True)

        # 윈도우 Resize, Move
        def moveWindow(event):
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # 위젯 Move
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)

        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.show()

    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    # closeEvent 발생시 무시하고 시스템 트레이로 이동
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "RS",
            "시스템 트레이로 이동합니다.",
            QSystemTrayIcon.Information,
            2000
        )


if __name__ == "__main__":

    # app_id를 가지고 중복 실행되지 않도록 Single application 으로 작동
    app_id = '20220727-RS-BA05-4277-8063-82A6DB9245A2'
    app = QtSingleApplication(app_id, sys.argv)
    if app.is_running():
        sys.exit(0)

    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')

    window = MainWindow()
    app.set_activate_window(window)

    sys.exit(app.exec_())