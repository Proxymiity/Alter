import sqlite3
from utils.dataIO import dataIO

db_loc = dataIO.load_json("data/sqlite.config.json")
db = sqlite3.connect(db_loc["file"])
dbc = db.cursor()


def sanitize(val):
    return "".join(x for x in val if x.isalnum())


def create_table(name: str):
    name = sanitize(name)
    dbc.execute("CREATE TABLE IF NOT EXISTS {}(sid INTEGER, name TEXT, value TEXT)".format(name))


def delete_table(name: str):
    name = sanitize(name)
    dbc.execute("DROP TABLE IF EXISTS {}".format(name))


def read(table: str, sid: int, name: str):
    table = sanitize(table)
    try:
        dbc.execute("SELECT value FROM {} WHERE sid=(?) AND name=(?)".format(table), (sid, name))
        value = dbc.fetchall()[0][0]
    except IndexError:
        value = None
    return value


def write(table: str, sid: int, name: str, value: str):
    table = sanitize(table)
    if read(table, sid, name) is None:
        dbc.execute("INSERT INTO {}(sid, name, value) VALUES (?, ?, ?)".format(table), (sid, name, value))
    else:
        dbc.execute("UPDATE {} SET value=(?) WHERE sid=(?) AND name=(?)".format(table), (value, sid, name))
    db.commit()


def delete(table: str, sid: int, name: str):
    table = sanitize(table)
    dbc.execute("DELETE FROM {} WHERE sid=(?) AND name=(?)".format(table), (sid, name))
    db.commit()
