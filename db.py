import sqlite3
import logging

def get_conn():
    return sqlite3.connect('bot.db')


def init_db():
    conn = get_conn()
    conn.execute("""CREATE TABLE mapping(
        group_name TEXT UNIQUE,
        channel_name TEXT UNIQUE
    )""")
    conn.commit()
    logging.info('The DB table created')


def get_slack_mappings():
    conn = get_conn()
    curs = conn.execute('''SELECT channel_name, group_name FROM mapping;''')
    mapping = dict(curs.fetchall())
    logging.debug("group mapping: %r", mapping)
    return mapping


def get_wechat_mappings():
    conn = get_conn()
    curs = conn.execute('''SELECT group_name, channel_name FROM mapping;''')
    return dict(curs.fetchall())


def del_mapping(group_name, channel_name):
    conn = get_conn()
    conn.execute('DELETE FROM mapping WHERE channel_name = ?;', (channel_name, ))
    conn.execute('DELETE FROM mapping WHERE group_name = ?;', (group_name, ))
    conn.commit()


def set_mapping(group_name, channel_name):
    conn = get_conn()
    del_mapping(group_name, channel_name)
    conn.execute('INSERT INTO mapping (group_name, channel_name) VALUES (?, ?);', (group_name, channel_name))
    conn.commit()


if __name__ == '__main__':
    init_db()
