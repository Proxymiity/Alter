import json
import os
from random import randint


class DataIO:
    def save_json(self, filename, data):
        rnd = randint(1000, 9999)
        path, ext = os.path.splitext(filename)
        tmp_file = "{}-{}.tmp".format(path, rnd)
        self._save_json(tmp_file, data)
        try:
            self._read_json(tmp_file)
        except json.decoder.JSONDecodeError:
            print("JSON integrity check on temp file for {} has failed. Original file unaltered.".format(filename))
            return False
        os.replace(tmp_file, filename)
        return True

    def load_json(self, filename):
        return self._read_json(filename)

    def is_valid_json(self, filename):
        try:
            self._read_json(filename)
            return True
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError:
            return False

    def _read_json(self, filename):
        with open(filename, encoding='utf-8', mode="r") as f:
            data = json.load(f)
        return data

    def _save_json(self, filename, data):
        with open(filename, encoding='utf-8', mode="w") as f:
            json.dump(data, f, indent=4, sort_keys=True,
                      separators=(',', ' : '))
        return data

    def export_json(self, data):
        return json.dumps(data)

    def import_json(self, data):
        return json.loads(data)


dataIO = DataIO()
