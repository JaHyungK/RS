# -*- coding: utf-8 -*-

from PySide2.QtCore import *
from PySide2.QtWidgets import *

from thread_rs import Thread


class Result(object):

    def __init__(self, did, dtime, table, path, file, access_mask, res, nickname, ip):
        self.id = did
        self.time = dtime
        self.table = table
        self.path = path
        self.file = file
        self.access_mask = access_mask
        self.res = res
        self.nickname = nickname
        self.ip = ip


class RsWindow(QWidget):
    get_threadEvent = Signal()
    get_threadEvent_clear = Signal()

    def __init__(self, *args, **kwargs):
        super(RsWindow, self).__init__(*args, **kwargs)

        self.row = 0

        self.restart_thread()

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QHBoxLayout(self)
        self.dataEngineGLayout = QGridLayout()
        self.dataEngineGLayout.setObjectName(u'SearchEngineLayout')

        self.tableWidget_data_info = QTableWidget()
        self.tableWidget_data_info.setObjectName(u"데이터 정보 테이블 위젯")

        self.header = self.tableWidget_data_info.horizontalHeader()
        self.header.setStretchLastSection(True)

        self._HEADER = {
            'tableWidget_local': {
                'header': ["아이디", "시간", "테이블", "경로", "파일", "엑세스 마스크", "결과", "사용자", "아이피"],
                'size': [90, 200, 150, 620, 300, 120, 50, 90]
            }, }

        headers = self._HEADER.get('tableWidget_local')
        headers = headers.get('header')

        self.tableWidget_data_info.setStyleSheet("background-color: #f5f5f5;\n"
                                                 "color: Black;")
        self.tableWidget_data_info.setColumnCount(9)
        self.tableWidget_data_info.setSortingEnabled(True)
        self.tableWidget_data_info.setHorizontalHeaderLabels(headers)
        self.tableWidget_data_info.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_data_info.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget_data_info.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for idx, width in enumerate(self._HEADER['tableWidget_local']['size']):
            self.tableWidget_data_info.setColumnWidth(idx, width)

        self.dataEngineGLayout.addWidget(self.tableWidget_data_info, 0, 0, 1, 1)

        # 재시작 버튼 레이아웃
        self.restart_HLayout = QHBoxLayout()
        self.restart_HLayout.setObjectName(u"restartHLayout")

        self.restartlabel = QLabel()
        self.restartlabel.setObjectName(u"label")
        self.restartlabel.setMinimumSize(QSize(0, 25))

        self.restart_PB = QPushButton('재시작')
        self.restart_PB.setStyleSheet("border-style: solid;\n"
                                                  "border-width: 1px;\n"
                                                  "font-size: 10.5pt;\n"
                                                  "heigth: 20px;\n"
                                                  "border-color: Dark Gray")
        self.restart_PB.setObjectName(u'재시작 버튼')
        self.restart_PB.setMinimumSize(QSize(135, 35))

        self.restart_PB.clicked.connect(self.restart_thread)
        self.restart_Spacer = QSpacerItem(50, 30, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        self.restart_HLayout.addItem(self.restart_Spacer)
        self.restart_HLayout.addWidget(self.restartlabel)
        self.restart_HLayout.addWidget(self.restart_PB)

        self.dataEngineGLayout.addLayout(self.restart_HLayout, 1, 0, 1, 1)

        self.main_layout.addLayout(self.dataEngineGLayout)

    def _clear_data_info(self, clear_message):
        """
        쓰레드가 재시작 될때 테이블 위젯에 보여지는 데이터를 삭제한다.
        """
        if clear_message == "clear_start":
            for row in range(self.tableWidget_data_info.rowCount()):
                self.tableWidget_data_info.removeRow(row)

    def _get_data_list(self, result_message):
        """
        수정, 삭제된 데이터에 대한 정보를 가공해서 테이블 위젯에 보여준다.
        """
        result_message = result_message.replace("(", "").replace(")", "").replace("'", "")
        result_message = result_message.split(',')
        rem = result_message

        results = []

        if rem is not None:

            r = Result(rem[0], rem[1], rem[2], rem[3], rem[4], rem[5], rem[6], rem[7], rem[8])
            results.append(r)

        for row, r in enumerate(results):
            self.tableWidget_data_info.insertRow(row)
            item0 = QTableWidgetItem(r.id)
            item1 = QTableWidgetItem(r.time)
            item2 = QTableWidgetItem(r.table)
            item3 = QTableWidgetItem(r.path)
            item4 = QTableWidgetItem(r.file)
            item5 = QTableWidgetItem(r.access_mask)
            item6 = QTableWidgetItem(r.res)
            item7 = QTableWidgetItem(r.nickname)
            item8 = QTableWidgetItem(r.ip)
            self.tableWidget_data_info.setItem(row, 0, item0)
            self.tableWidget_data_info.setItem(row, 1, item1)
            self.tableWidget_data_info.setItem(row, 2, item2)
            self.tableWidget_data_info.setItem(row, 3, item3)
            self.tableWidget_data_info.setItem(row, 4, item4)
            self.tableWidget_data_info.setItem(row, 5, item5)
            self.tableWidget_data_info.setItem(row, 6, item6)
            self.tableWidget_data_info.setItem(row, 7, item7)
            self.tableWidget_data_info.setItem(row, 8, item8)

    ##### 쓰레드 부분 #####
    def _clear(self):
        self._clear_data_info()

    def restart_thread(self):

        self.th = Thread(parent=self)

        if self.th.isRun:
            print('메인 : 쓰레드 정지')
            self.th.quit()
            self.th.wait(0.15)
            self.th.isRun = False

        if not self.th.isRun:
            print('메인 : 쓰레드 시작')
            self.th.start()
            self.th.threadEvent_clear.connect(self._clear_data_info)
            self.th.threadEvent.connect(self._get_data_list)
            self.th.isRun = True