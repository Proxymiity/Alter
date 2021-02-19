import os
import shutil
from pathlib import Path
from utils.dataIO import dataIO

fe = ".json"
db_path = dataIO.load_json("data/file.config.json")["path"]
path = Path(os.getcwd() + "/" + db_path)


def init_storage(p: Path):
    if not p.is_dir() and p.exists():
        shutil.rmtree(str(p))
        os.makedirs(str(p))
    if not p.exists():
        os.makedirs(str(p))


def load_file(p: str):
    try:
        return dataIO.load_json(p)
    except FileNotFoundError:
        return None


def sanitize(val):
    return "".join(x for x in val if x.isalnum())


def create_table(name: str):
    init_storage(path)
    name = sanitize(name)
    t_path = Path(str(path) + "/" + name)
    os.makedirs(t_path)


def delete_table(name: str):
    name = sanitize(name)
    t_path = Path(str(path) + "/" + name)
    shutil.rmtree(str(t_path))


def read(table: str, sid: int, name: str):
    table = sanitize(table)
    d_rel = "/" + table + "/" + str(sid) + fe
    d_data = load_file(db_path + d_rel)
    if d_data is None:
        return None
    else:
        try:
            return d_data[name]
        except KeyError:
            return None


def write(table: str, sid: int, name: str, value: str):
    table = sanitize(table)
    d_rel = "/" + table + "/" + str(sid) + fe
    d_data = load_file(db_path + d_rel) or {}
    d_data[name] = value
    dataIO.save_json(db_path + d_rel, d_data)


def delete(table: str, sid: int, name: str):
    table = sanitize(table)
    d_rel = "/" + table + "/" + str(sid) + fe
    d_data = load_file(db_path + d_rel)
    if d_data is None:
        return
    d_data[name] = None
    dataIO.save_json(db_path + d_rel, d_data)
