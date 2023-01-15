# -*- coding: utf-8 -*-
import os
import sys

from PySide2.QtCore import *
from core.db import *

import subprocess
import time
import re
import datetime as dt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 공유폴더 이벤트 로그 보여주는 Posershell 명령어
cmd = "powershell Get-WinEvent -FilterHashtable @{logname = 'security';id=5145; data = " \
      "'0x2', '0x4', '0x20','00120089', '0x110080', '0x10080'}  " \
      "| Sort-Object TimeCreated -Descending | Format-Table TimeCreated, Message -wrap"


class Thread(QThread):

    # 쓰레드 시그널 이벤트 변수
    threadEvent = Signal(str)
    threadEvent_clear = Signal(str)

    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)

        self.parent = parent

        self.isRun = False

    def stop(self):
        self.quit()
        self.wait(3)
        self.isRun = False

    def run(self):
        """
        이벤트 로그를 얻기 위해 thread를 실행한다.
        """
        while self.isRun:
            # 테이블 위젯이 Clear 되도록 signal 전송
            self.send_threadEvent_clear("clear_start")

            # 이벤트 로그를 얻는 함수 실행
            try:
                self._get_event_log(cmd)
            except subprocess.CalledProcessError as e:
                error_info = "command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output)
                return error_info

            # 불필요한 과부하를 방지하기 위해 80초마다 재실행
            time.sleep(80)

    def send_threadEvent_clear(self, clear_message):
        """
        테이블 위젯을 clear 하기 위해 메세지를 전송하는 메소드
        """
        self.threadEvent_clear.emit(str(clear_message))

    def send_threadEvent(self, res):
        """
        테이블 위젯에 이벤트 로그를 보여주기 위해 메세지를 전송하는 메소드
        """
        self.threadEvent.emit(str(res))

    def _get_server_ip(self):
        """
        해당 파일서버의 아이피를 얻는 함수
        """
        import socket
        ip_addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_addr.connect(("8.8.8.8", 443))
        ip_addr = ip_addr.getsockname()[0]
        return ip_addr

    def _do_insert(self, log_table, event_log):
        """
        db 테이블에 로그를 삽입한다.
        """
        insert_data(self, log_table, event_log)

    def _distinguish_table(self, result, event_log):
        """
        조건에 맞게 DB테이블을 구분한다.
        """
        _drive_name = event_log[3]

        # 조건에 맞으면 M 드라이브 테이블로 로그 데이터 삽입
        if _drive_name == 'M_drive' and self._get_server_ip() == '192.168.219.104':
            if result == 'DELETE':
                log_table = 'delete_move_m'
            else:
                log_table = 'modified_m'

        self._do_insert(log_table, event_log)

        # 조건에 맞으면 X 드라이브 테이블로 로그 데이터 삽입
        if _drive_name == 'X_drive' and self._get_server_ip() == '192.168.219.104':
            if result == 'DELETE':
                log_table = 'delete_move_x'
            else:
                log_table = 'modified_x'

        self._do_insert(log_table, event_log)

    def _parsing_inform(self, log_attr, file_name):
        """
        리스트의 요소에서 제목은 잘라내고 값만 추출한다.
        """
        date = None
        user_ip = None
        shared_folder = None
        shared_path = None
        access_mask = None

        path, file = os.path.split(file_name)
        for line in log_attr:
            line = line.strip()
            if line.startswith('오전') or line.startswith('오후'):
                date = dt.datetime.now().strftime('%Y-%m-%d')
                time_line = line
                time_line = time_line.split(' 클라이언트에 원하는')
                time_line = time_line[0]
                date = date + ' ' + time_line
            if line.startswith('원본 주소'):
                user_ip = line.strip('원본 주소:		')
            if line.startswith('공유 경로'):
                shared_line = line.strip('공유 경로:		    ')
                shared_line = shared_line.split("\\")
                if len(shared_line) == 4:
                    shared_path, shared_folder = shared_line[3], shared_line[2]
                    shared_folder = shared_folder[0]
            if line.startswith('액세스 마스크:'):
                access_mask_line = line
                access_mask = access_mask_line.strip('액세스 마스크:		')
            if line.startswith('액세스:'):
                result_line = line
                result = result_line.strip('액세스:		')
                if result == 'DELETE' or result == 'WriteData (또는 AddFile)' \
                        or result == 'AppendData (또는 AddSubdirectory 또는 CreatePipeInstance)':
                    event_log = [date, user_ip, shared_folder, shared_path, path, file, access_mask]
                    self._distinguish_table(result, event_log)

    def _get_file_name(self, string):
        """
        문단으로 자른 string에서 파일 이름을 얻는다.
        """
        try:
            # 칸으로 string 분리
            log_attr = re.split('\n+', string)

            # for문을 돌려 리스트 요소 안에 상대 대상 이름을 포함하고 있는 요소를 찾기
            for res in log_attr:
                if '상대 대상 이름' in res:
                    # 상대 대상 이름을 기준으로 분리
                    file_name = re.split('상대 대상 이름:', res, 1)
                    # 공백 패턴 컴파일
                    pattern = re.compile(r'[\s]+')
                    # 공백 제거
                    file_name = re.sub(pattern, '', str(file_name[1]), 1)

            self._parsing_inform(log_attr, file_name)
        except ValueError:
            pass

    def _get_event_log(self, cmd):
        """
        출력되는 데이터를 날짜 기준 문단으로 자른다.
        """
        res = subprocess.check_output(cmd).decode('euc-kr')
        res = reversed(re.split('\d\d\d\d-\d\d-\d\d', res))
        for string in res:
            # 파일이 생성, 삭제, 이동, 파일 업로드, 복사, 파일명이 변경 되었을 경우
            if 'DELETE' in string or 'SYNCHRONIZE' in string:
                self._get_file_name(string)
            # 파일 수정, 내용 변경, 생성, 파일 업로드, 복사 되었을 경우
            if 'WriteData' in string and 'AppendData' not in string:
                self._get_file_name(string)
            if 'AppendData' in string and 'WriteData' not in string:
                self._get_file_name(string)

        # 윈도우 언어가 기본 언어가 UTF-8 로 설정되어 있을 경우 아래 코드를
        # res = res.decode('utf-8').split('\n')

        # 기본언어가 한국어 euc-kr 되어있을 경우는 아래 코드로
        # res = res.decode('euc-kr').split('\r')
        # res = res.split('\n')
