import json
import os
from random import randint


class DataIO:
    def save_json(self, filename, data):
        rnd = randint(1000, 9999)
        path, ext = os.path.splitext(filename)
        tmp_file = f"{path}-{rnd}.tmp"
        self._save_json(tmp_file, data)
        try:
            self._read_json(tmp_file)
        except json.decoder.JSONDecodeError:
            print(f"JSON integrity check on temp file for {filename} has failed. Original file unaltered.")
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

    @staticmethod
    def _read_json(filename):
        with open(filename, encoding='utf-8', mode="r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def _save_json(filename, data):
        with open(filename, encoding='utf-8', mode="w") as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
        return data

    @staticmethod
    def export_json(data):
        return json.dumps(data)

    @staticmethod
    def import_json(data):
        return json.loads(data)


dataIO = DataIO()
