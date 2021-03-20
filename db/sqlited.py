import sqlite3
from utils.dataIO import dataIO

db_loc = dataIO.load_json("data/sqlite.config.json")
db = sqlite3.connect(db_loc["file"])
dbc = db.cursor()


def sanitize(val):
    return "".join(x for x in val if x.isalnum())


def create_table(name: str):
    name = sanitize(name)
    dbc.execute(f"CREATE TABLE IF NOT EXISTS {name}(sid INTEGER, name TEXT, value TEXT)")


def delete_table(name: str):
    name = sanitize(name)
    dbc.execute(f"DROP TABLE IF EXISTS {name}")


def read(table: str, sid: int, name: str):
    table = sanitize(table)
    try:
        dbc.execute(f"SELECT value FROM {table} WHERE sid=(?) AND name=(?)", (sid, name))
        value = dbc.fetchall()[0][0]
    except IndexError:
        value = None
    return value


def write(table: str, sid: int, name: str, value: str):
    table = sanitize(table)
    if read(table, sid, name) is None:
        dbc.execute(f"INSERT INTO {table}(sid, name, value) VALUES (?, ?, ?)", (sid, name, value))
    else:
        dbc.execute(f"UPDATE {table} SET value=(?) WHERE sid=(?) AND name=(?)", (value, sid, name))
    db.commit()


def delete(table: str, sid: int, name: str):
    table = sanitize(table)
    dbc.execute(f"DELETE FROM {table} WHERE sid=(?) AND name=(?)", (sid, name))
    db.commit()
