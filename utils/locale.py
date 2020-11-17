from utils.dataIO import dataIO
import os


def load(lang, module):
    file = "locales/{}/{}.json".format(lang, module)
    if os.path.isfile(file):
        return dataIO.load_json(file)
    else:
        print("Locale {}/{} not found!".format(lang, module))
        settings = dataIO.load_json("data/locale.json")  # todo merge locale.json and config.json as fallback_lang?
        file = "locales/" + settings["fallback"] + "/{}.json".format(module)
        return dataIO.load_json(file)
