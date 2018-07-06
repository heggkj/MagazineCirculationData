import sqlite3 as lite


def add_row_to_magazines(database_path: str, title_code: str, reported_title: str):
    conn = lite.connect(database_path)
    with conn:
        cur = conn.cursor()
        sql = f'select count(reported_title) from magazines where reported_title = \"{reported_title}\"'
        cur.execute(sql)
        count = cur.fetchone()[0]
        if count < 1:
            sql = f'insert into magazines(title_code, reported_title) values(\"{title_code}\", \"{reported_title}\")'
            cur.execute(sql)
    conn.close()


def add_row_to_title_audit(database_path: str, title_code: str, reported_title: str, file_name: str):
    conn = lite.connect(database_path)
    with conn:
        cur = conn.cursor()
        sql = f'insert into title_audit(title_code, reported_title, file_name) values(\"{title_code}\", ' \
              f'\"{reported_title}\", \"{file_name}\") '
        cur.execute(sql)
    conn.close()

