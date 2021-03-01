from utils.dataIO import dataIO
import os
from importlib import import_module
db = import_module(dataIO.load_json("data/config.json")["storage"])


def get(ctx, mod, key):
    if ctx.guild:
        loc = db.read("serversettings", ctx.guild.id, "locale") or db.read("settings", 0, "locale")
    else:
        loc = db.read("settings", 0, "locale")
    return load(loc, mod, key)


def load(locale, module, key):
    file = "locales/{}/{}.json".format(locale, module)
    if os.path.isfile(file):
        try:
            return dataIO.load_json(file)[key]
        except KeyError:
            return "Missing locale {}.{}-{}".format(module, key, locale)
    else:
        return "Missing module {}.{}-{}".format(module, key, locale)
