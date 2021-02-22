from utils.dataIO import dataIO
from importlib import import_module
config = dataIO.load_json("data/config.json")
db = import_module(config["storage"])
db_d = {"name": "Alter", "prefix": "::", "locale": "fr_FR"}


def check():
    db.create_table("server_settings")
    db.create_table("settings")
    for x in db_d:
        if not db.read("settings", 0, x):
            db.write("settings", 0, x, db_d[x])
