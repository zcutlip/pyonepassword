import fnmatch
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict
from configparser import ConfigParser

whitelist = ["output", "*.txt", "*.json"]


class TextFile:
    def __init__(self, file_path, sanitization_map: Dict[str, str]):
        self._smap = sanitization_map
        self._fpath = file_path

    def sanitize(self):
        print(f"Sanitizing {self._fpath}")
        changed = False
        try:
            text = open(self._fpath, "r").read()
        except UnicodeDecodeError:
            print("\tnot text")
            return changed
        for old, new in self._smap.items():
            if old in text:
                text = text.replace(old, new)
                changed = True
        if changed:
            print("\tSanitized")
            open(self._fpath, "w").write(text)
        else:
            print("\tNo change")
        return changed


def sanitize_files(top_dir, sanitization_map):

    for root, dirs, files in os.walk(top_dir):
        for file in files:
            for pattern in whitelist:
                if fnmatch.fnmatch(file, pattern):
                    textfile = TextFile(Path(root, file), sanitization_map)
                    textfile.sanitize()


def sanitize_parse_args():
    parser = ArgumentParser()
    parser.add_argument("config", help="Path to config file")

    parsed = parser.parse_args()
    return parsed


def main():
    args = sanitize_parse_args()
    config_path = args.config
    config = ConfigParser()
    config.optionxform = str
    config.read(config_path)
    tests_path = config['main']['tests_path']
    responses_path = config['main']['response-path']
    responses_path = Path(tests_path, responses_path)
    data_path = config['main']['test_data_path']
    data_path = Path(tests_path, data_path)
    replacement_map = dict(config['replacements'])

    for path in [responses_path, data_path]:
        sanitize_files(path, replacement_map)


if __name__ == "__main__":
    main()
