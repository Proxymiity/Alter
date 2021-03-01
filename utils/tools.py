import discord
from utils.dataIO import dataIO
from importlib import import_module
config = dataIO.load_json("data/config.json")
db = import_module(config["storage"])
tb_d = ["serversettings", "settings"]
db_d = {"name": "Alter", "prefix": "::", "locale": "en_US", "status": "online",
        "presence_type": "game", "presence_value": "::help"}


def check_defaults():
    for t in tb_d:
        db.create_table(t)
    db.delete_table("temp")
    db.create_table("temp")
    for x in db_d:
        if not db.read("settings", 0, x):
            db.write("settings", 0, x, db_d[x])


def get_presence(p_type, p_val):
    if p_type == "none":
        return None
    elif p_type == "game":
        return discord.Game(p_val)
    elif p_type == "listen":
        return discord.Activity(name=p_val, type=discord.ActivityType.listening)
    elif p_type == "watch":
        return discord.Activity(name=p_val, type=discord.ActivityType.watching)
    elif p_type == "compete":
        return discord.Activity(name=p_val, type=discord.ActivityType.competing)
    elif p_type == "stream":
        s = p_val.split(";", 1)
        return discord.Streaming(name=s[1], url=s[0])


def get_status(status):
    if status == "online":
        return discord.Status.online
    elif status == "idle":
        return discord.Status.idle
    elif status == "dnd":
        return discord.Status.dnd
    elif status == "offline":
        return discord.Status.offline