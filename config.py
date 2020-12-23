from utils.dataIO import dataIO
import sys

args = sys.argv
config = {}  # Only to satisfy CodeQL requirements

try:
    config = dataIO.load_json("data/config.json")
except FileNotFoundError:
    print("Missing data/config.json file. Aborting.")
    exit(1)

if len(args) == 1:
    print("config.py: small utility to edit the configuration (for use with CLI/")
    print("- ./{}: show config".format(args[0]))
    print("- ./{} <key>: show config for a specific key".format(args[0]))
    print("- ./{} <key> <value>: set config for a specific key".format(args[0]))
    print("To set value lists please edit the config manually (there isn't that much lists)")
    print("")
    print("Current configuration is:")
    for i in config:
        print("{0}: {1}".format(i, config[i]))
    exit(0)

if len(args) == 2:
    try:
        print("{0}: {1}".format(args[1], config[args[1]]))
    except KeyError:
        print("'{}' is not present in the data/config.json file.".format(args[1]))
        print("Hint: Values are case-sensitive, please make sure you typed the value correctly.")
        exit(2)

if len(args) > 2:
    try:
        config[args[1]]
    except KeyError:
        print("'{}' is not present in the data/config.json file.".format(args[1]))
        print("Hint: Values are case-sensitive, please make sure you typed the value correctly.")
        exit(2)
    if isinstance(config[args[1]], (list, dict)):
        print("Cannot edit lists or dicts, please open the config file yourself.")
        exit(3)
    if isinstance(config[args[1]], int):
        config[args[1]] = int(args[2])
    else:
        value = " ".join(args[2:])
        config[args[1]] = value
    dataIO.save_json("data/config.json", config)
    print("Successfully set and saved value.")
    exit(0)
