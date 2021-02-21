from utils.dataIO import dataIO
import sys

args = sys.argv
config = {}  # Only to satisfy CodeQL requirements

if len(args) == 1:
    print("config.py: small utility to edit the configuration (for use with CLI)")
    print("- ./{} <file>: show config for file".format(args[0]))
    print("- ./{} <file> <key>: show config for a specific key".format(args[0]))
    print("- ./{} <file> <key> <value>: set config for a specific key".format(args[0]))
    print("Example: ./{} config owner 481038581032403850".format(args[0]))
    print("To set value lists please edit the config manually (there isn't that much lists)")
    exit(0)

try:
    config = dataIO.load_json("data/" + str(args[1]) + ".json")
except FileNotFoundError:
    print("Missing data/{}.json file. Aborting.".format(args[1]))
    exit(1)

if len(args) == 2:
    print("Current configuration for data/{}.json is:".format(args[1]))
    for i in config:
        print("{0}: {1}".format(i, config[i]))
    exit(0)

if len(args) == 3:
    try:
        print("{0}: {1}".format(args[2], config[args[2]]))
    except KeyError:
        print("'{}' is not present in the data/{}.json file.".format(args[2], args[1]))
        print("Hint: Values are case-sensitive, please make sure you typed the value correctly.")
        exit(2)

if len(args) > 3:
    try:
        config[args[2]]
    except KeyError:
        print("'{}' is not present in the data/{}.json file.".format(args[2], args[1]))
        print("Hint: Values are case-sensitive, please make sure you typed the value correctly.")
        exit(2)
    if isinstance(config[args[2]], (list, dict)):
        print("Cannot edit lists or dicts, please open the config file yourself.")
        exit(3)
    if isinstance(config[args[2]], int):
        config[args[2]] = int(args[3])
    else:
        value = " ".join(args[3:])
        config[args[2]] = value
    dataIO.save_json(str(args[1]), config)
    print("Successfully set and saved value.")
    exit(0)
