import os
from utils import db
from utils.dataIO import dataIO


def get(ctx, mod, key):
    if ctx.guild:
        loc = db.read("serversettings", ctx.guild.id, "locale") or db.read("settings", 0, "locale")
    else:
        loc = db.read("settings", 0, "locale")
    return load(loc, mod, key)


def load(locale, module, key):
    file = f"locales/{locale}/{module}.json"
    if os.path.isfile(file):
        try:
            return dataIO.load_json(file)[key]
        except KeyError:
            return f"Missing locale {module}.{key}-{locale}"
    else:
        return f"Missing module {module}.{key}-{locale}"
