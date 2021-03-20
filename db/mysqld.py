import mysql.connector
from utils.dataIO import dataIO

db_cfg = dataIO.load_json("data/mysql.config.json")
db = mysql.connector.connect(host=db_cfg["host"], autocommit=True,
                             user=db_cfg["user"], password=db_cfg["pass"], database=db_cfg["db"])
dbc = db.cursor()


def sanitize(val):
    return "".join(x for x in val if x.isalnum())


def check():
    if not db.is_connected():
        db.reconnect()


def create_table(name: str):
    check()
    name = sanitize(name)
    dbc.execute(f"CREATE TABLE IF NOT EXISTS {name}(sid BIGINT UNSIGNED, name TEXT, value TEXT)")


def delete_table(name: str):
    check()
    name = sanitize(name)
    dbc.execute("SET foreign_key_checks = 0")
    dbc.execute(f"DROP TABLE IF EXISTS {name}")
    dbc.execute("SET foreign_key_checks = 1")


def read(table: str, sid: int, name: str):
    check()
    table = sanitize(table)
    try:
        dbc.execute(f"SELECT value FROM {table} WHERE sid=%s AND name=%s", (sid, name))
        value = dbc.fetchall()[0][0]
    except IndexError:
        value = None
    return value


def write(table: str, sid: int, name: str, value: str):
    check()
    table = sanitize(table)
    if read(table, sid, name) is None:
        dbc.execute(f"INSERT INTO {table}(sid, name, value) VALUES (%s, %s, %s)", (sid, name, value))
    else:
        dbc.execute(f"UPDATE {table} SET value=%s WHERE sid=%s AND name=%s", (value, sid, name))


def delete(table: str, sid: int, name: str):
    check()
    table = sanitize(table)
    dbc.execute(f"DELETE FROM {table} WHERE sid=%s AND name=%s", (sid, name))
