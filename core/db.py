# -*- coding: utf-8 -*-

import mysql.connector

_HOST = u''
_PASSWORD = u''


def get_con_data_info(db='data_info'):

    conn = None

    if conn is None:
        conn = mysql.connector.connect(
            host=_HOST,
            user='root',
            password=_PASSWORD,
            db=db,
            charset='utf8'
        )
    return conn


def get_con_smart_maker(db='smart_maker'):

    conn = None

    if conn is None:
        conn = mysql.connector.connect(
            host=_HOST,
            user='root',
            password=_PASSWORD,
            db=db,
            charset='utf8'
        )
    return conn


def get_name_from_ip(ip):
    conn = get_con_smart_maker()
    curs = conn.cursor()
    sql = 'SELECT name FROM users WHERE ip LIKE %s'
    curs.execute(sql, (ip,))

    res = curs.fetchall()
    conn.close()
    if res:
        res = [list(res[x]) for x in range(len(res))]
        res = res[0][0]
        res = str(res)

        return res


def insert_data(self, data_table, event_log):

    date = event_log[0]
    user_ip = event_log[1]
    shared_folder = event_log[2]
    shared_path = event_log[3]
    path = event_log[4]
    file = event_log[5]
    access_mask = event_log[6]

    conn = get_con_data_info()
    curs = conn.cursor()
    select_path = path.replace('\\', '\\\\')
    sql = 'INSERT INTO ' \
          '{} (date_time, user_ip, shared_folder, shared_path, path, file, access_mask) ' \
          'SELECT ' \
          '%s, %s, %s, %s, %s, %s , %s ' \
          'FROM DUAL WHERE NOT EXISTS ' \
          '(SELECT * FROM {} ' \
          'WHERE ' \
          'date_time = "{}" ' \
          'AND user_ip = "{}" ' \
          'AND shared_folder = "{}" ' \
          'AND shared_path = "{}" ' \
          'AND path = "{}" ' \
          'AND file = "{}" ' \
          'AND access_mask = "{}")' \
          ''.format(data_table, data_table, date, user_ip, shared_folder, shared_path, select_path, file,
                    access_mask)
    curs.execute(sql, (date, user_ip, shared_folder, shared_path, path, file, access_mask))
    conn.commit()

    nickname = get_name_from_ip(user_ip)

    if curs.rowcount is not 0:
        res = curs.lastrowid, date, data_table, path, file, access_mask, "성공", nickname, user_ip

        # 테이블에 삽입된 데이터를 테이블 위젯에 보여주기 위해 Signal 전송
        self.send_threadEvent(res)
    else:
        pass

    conn.close()

