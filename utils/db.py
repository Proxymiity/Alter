from utils.dataIO import dataIO
from importlib import import_module
driver = import_module(dataIO.load_json("data/config.json")["storage"])
tb_d = ["serversettings", "settings"]
db_d = {"name": "Alter", "prefix": "::", "locale": "en_US", "status": "online",
        "presence_type": "game", "presence_value": "::help"}


def check_defaults():
    for t in tb_d:
        create_table(t)
    delete_table("temp")
    create_table("temp")
    for x in db_d:
        if not read("settings", 0, x):
            write("settings", 0, x, db_d[x])


def create_table(name: str):
    driver.create_table(name)


def delete_table(name: str):
    driver.delete_table(name)


def read(table: str, sid: int, name: str) -> str:
    return driver.read(table, sid, name)


def write(table: str, sid: int, name: str, value: str):
    driver.write(table, sid, name, value)


def delete(table: str, sid: int, name: str):
    driver.delete(table, sid, name)


check_defaults()
