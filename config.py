from utils.dataIO import dataIO
import sys

args = sys.argv
config = {}  # Only to satisfy CodeQL requirements

if len(args) == 1:
    print("config.py: small utility to edit the configuration (for use with CLI)")
    print(f"- ./{args[0]} <file>: show config for file")
    print(f"- ./{args[0]} <file> <key>: show config for a specific key")
    print(f"- ./{args[0]} <file> <key> <value>: set config for a specific key")
    print(f"Example: ./{args[0]} config owner 481038581032403850")
    print("To set value lists please edit the config manually (there isn't that much lists)")
    exit(0)

try:
    config = dataIO.load_json("data/" + str(args[1]) + ".json")
except FileNotFoundError:
    print(f"Missing data/{args[1]}.json file. Aborting.")
    exit(1)

if len(args) == 2:
    print(f"Current configuration for data/{args[1]}.json is:")
    for i in config:
        print(f"{i}: {config[i]}")
    exit(0)

if len(args) == 3:
    try:
        print(f"{args[2]}: {config[args[2]]}")
    except KeyError:
        print(f"'{args[2]}' is not present in the data/{args[1]}.json file.")
        print("Hint: Values are case-sensitive, please make sure you typed the value correctly.")
        exit(2)

if len(args) > 3:
    try:
        config[args[2]]
    except KeyError:
        print(f"'{args[2]}' is not present in the data/{args[1]}.json file.")
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
    dataIO.save_json(str("data/" + str(args[1]) + ".json"), config)
    print("Successfully set and saved value.")
    exit(0)
