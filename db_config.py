import sys
from utils.dataIO import dataIO
from importlib import import_module
from utils.tools import check_defaults
check_defaults()
db = import_module(dataIO.load_json("data/config.json")["storage"])
args = sys.argv

if len(args) == 1:
    print("db_config.py: small utility to input into the Alter database")
    print("this only allows to edit the 'settings' table")
    print(f"- ./{args[0]} <key>: show value for key")
    print(f"- ./{args[0]} <key> <value>: set value for key")
    print(f"Example: ./{args[0]} name Alter")

if len(args) == 2:
    val = db.read("settings", 0, args[1])
    if val:
        print(f"{args[1]}: {val}")
    else:
        print(f"'{args[1]}' is not present in the database.")
        print("Hint: Values are case-sensitive, please make sure you typed the value correctly.")
        exit(2)

if len(args) > 2:
    value = " ".join(args[2:])
    db.write("settings", 0, args[1], value)
    print("Value recorded to database.")
    exit(0)
