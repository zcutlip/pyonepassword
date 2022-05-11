import fnmatch
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict
from configparser import ConfigParser

whitelist = ["output", "*.txt", "*.json", "test_*.py"]


class TextFile:
    def __init__(self, file_path, sanitization_map: Dict[str, str]):
        self._smap = sanitization_map
        self._fpath = file_path

    def sanitize(self):
        changed = False
        try:
            text = open(self._fpath, "r").read()
        except UnicodeDecodeError:
            return changed
        for old, new in self._smap.items():
            if old in text:
                text = text.replace(old, new)
                changed = True
        if changed:
            print(f"Sanitized {self._fpath}")
            open(self._fpath, "w").write(text)

        return changed


def sanitize_files(top_dir, sanitization_map):
    changed_count = 0
    file_count = 0
    for root, dirs, files in os.walk(top_dir):
        for file in files:
            for pattern in whitelist:
                if fnmatch.fnmatch(file, pattern):
                    textfile = TextFile(Path(root, file), sanitization_map)
                    file_count += 1
                    if textfile.sanitize():
                        changed_count += 1
    print(f"Considered {file_count} files")
    print(f"Changed {changed_count} files")


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
    # responses_path = config['main']['response-path']
    # responses_path = Path(tests_path, responses_path)
    # data_path = config['main']['test_data_path']
    # data_path = Path(tests_path, data_path)
    replacement_map = dict(config['replacements'])

    sanitize_files(tests_path, replacement_map)


if __name__ == "__main__":
    main()
