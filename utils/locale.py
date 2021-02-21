from utils.dataIO import dataIO
import os


def get(ctx, db, mod, key):
    if ctx.guild:
        loc = db.read("server_settings", ctx.guild.id, "locale") or db.read("settings", 0, "locale")
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
