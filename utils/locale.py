from utils.dataIO import dataIO
import os


def load(locale, module):
    file = "locales/{}/{}.json".format(locale, module)
    if os.path.isfile(file):
        return dataIO.load_json(file)
    else:
        print("Locale {}/{} not found!".format(locale, module))
        config = dataIO.load_json("data/config.json")
        file = "locales/" + config["fallback_locale"] + "/{}.json".format(module)
        return dataIO.load_json(file)
