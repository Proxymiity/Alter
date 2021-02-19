import mysql.connector
from utils.dataIO import dataIO

db_cfg = dataIO.load_json("data/mysql.config.json")
db = mysql.connector.connect(host=db_cfg["host"],
                             user=db_cfg["user"], password=db_cfg["pass"], database=db_cfg["db"])
dbc = db.cursor()


def create_table(name: str):
    dbc.execute("CREATE TABLE IF NOT EXISTS {}(sid INTEGER, name TEXT, value TEXT)".format(name))


def delete_table(name: str):
    dbc.execute("SET foreign_key_checks = 0")
    dbc.execute("DROP TABLE IF EXISTS {}".format(name))
    dbc.execute("SET foreign_key_checks = 1")


def read(table: str, sid: int, name: str):
    try:
        dbc.execute("SELECT value FROM {} WHERE sid={} AND name='{}'".format(table, sid, name))
        value = dbc.fetchall()[0][0]
    except IndexError:
        value = None
    return value


def write(table: str, sid: int, name: str, value: str):
    if read(table, sid, name) is None:
        dbc.execute("INSERT INTO {}(sid, name, value) VALUES ({}, '{}', '{}')".format(table, sid, name, value))
    else:
        dbc.execute("UPDATE {} SET value='{}' WHERE sid={} AND name='{}'")
    db.commit()


def delete(table: str, sid: int, name: str):
    dbc.execute("DELETE FROM {} WHERE sid={} AND name='{}'".format(table, sid, name))
    db.commit()
