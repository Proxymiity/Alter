from utils.dataIO import dataIO
from importlib import import_module
config = dataIO.load_json("data/config.json")
db = import_module(config["storage"])
tb_d = ["serversettings", "settings"]
db_d = {"name": "Alter", "prefix": "::", "locale": "en_US"}


def check_defaults():
    for t in tb_d:
        db.create_table(t)
    db.delete_table("temp")
    db.create_table("temp")
    for x in db_d:
        if not db.read("settings", 0, x):
            db.write("settings", 0, x, db_d[x])
