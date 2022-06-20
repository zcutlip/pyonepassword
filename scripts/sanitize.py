import fnmatch
import json
import os
import re
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path
from typing import Dict

WHITELIST = ["output", "*.txt", "*.json", "*.py"]


class TextFile:
    def __init__(self, file_path, sanitization_map: Dict[str, str]):
        self._smap = sanitization_map
        self._fpath = file_path

    def sanitize(self):
        changed = False
        try:
            old_text = open(self._fpath, "r").read()
        except UnicodeDecodeError:
            return changed
        new_text = self._sanitize_str(old_text, self._smap)
        if old_text != new_text:
            changed = True
            print(f"Sanitized {self._fpath}")
            open(self._fpath, "w").write(new_text)

        return changed

    def _sanitize_str(self, string, sanitization_map: Dict[str, str]):
        for old, new in sanitization_map.items():
            if old in string:
                string = string.replace(old, new)
        return string


class JSONFile(TextFile):
    def sanitize(self):
        changed = False
        # get the indent of the original file
        # to prevent unneeded whitespace changes
        indent = self._detect_indent()
        json_text = open(self._fpath, "r").read()
        obj = json.loads(json_text)
        obj = self._sanitize_obj(obj, self._smap)
        new_json_text = json.dumps(obj, indent=indent)

        # json.dump() won't add a trailing newline, but the original file
        # may have had one (vscode appends one on save), so lets
        # append one if necessary to prevent unneeded file diffs
        if json_text.endswith("\n"):
            new_json_text += "\n"
        if json_text != new_json_text:
            changed = True
            with open(self._fpath, "w") as f:
                f.write(new_json_text)
        return changed

    def _detect_indent(self):
        indent = None
        lines = open(self._fpath, "r").readlines()
        if len(lines) >= 2:
            second_line = lines[1]
            match = re.match(r"^(\s+).+", second_line)
            if match:
                indent = match.groups()[0]
        return indent

    def _sanitize_obj(self, obj, sanitization_map: Dict[str, str]):
        if isinstance(obj, dict):
            obj = self._sanitize_dict(obj, sanitization_map)
        elif isinstance(obj, list):
            obj = self._sanitize_list(obj, sanitization_map)
        elif isinstance(obj, str):
            obj = self._sanitize_str(obj, sanitization_map)
        else:
            # some other type of obect we don't know how to (or need to?) sanitize
            pass
        return obj

    def _sanitize_dict(self, obj, sanitization_map):
        new_dict = {}
        for key, val in obj.items():
            key = self._sanitize_str(key, sanitization_map)
            if key in new_dict:
                pass
                # raise ValueError(f"Key already present in new dict: {key}")
            val = self._sanitize_obj(val, sanitization_map)
            new_dict[key] = val
        return new_dict

    def _sanitize_list(self, list_obj: list, sanitization_map: Dict[str, str]):
        new_list = []
        # duplicates = False
        # if len(list_obj) > len(set(list_obj)):
        #     duplicates = True

        for item in list_obj:
            new_item = self._sanitize_obj(item, sanitization_map)
            if new_item in new_list:  # and not duplicates:
                pass
                # print(self._fpath)
                # pprint(list_obj, sort_dicts=False, indent=2)
                # raise ValueError(f"Duplicate item in list {new_item}")
            new_list.append(new_item)
        return new_list


def _santize_single(filepath, sanitization_map, whitelist):
    changed = False
    considered = False
    for pattern in whitelist:
        if fnmatch.fnmatch(filepath, pattern):

            if filepath.suffix == ".json":
                textfile = JSONFile(filepath, sanitization_map)
            else:
                textfile = TextFile(filepath, sanitization_map)
            considered = True
            changed = textfile.sanitize()
    return (considered, changed)


def sanitize_files(sanitize_path, sanitization_map):
    changed_count = 0
    file_count = 0
    sanitize_path = Path(sanitize_path)
    local_whitelist = WHITELIST
    if sanitize_path.is_file():
        local_whitelist = [sanitize_path]
        considered, changed = _santize_single(
            sanitize_path, sanitization_map, local_whitelist)
        if considered:
            file_count += 1
        if changed:
            changed_count += 1
    else:
        for root, dirs, files in os.walk(sanitize_path):
            for file in files:
                filepath = Path(root, file)
                considered, changed = _santize_single(
                    filepath, sanitization_map, local_whitelist)
                if considered:
                    file_count += 1
                if changed:
                    changed_count += 1

    print(f"Considered {file_count} files")
    print(f"Changed {changed_count} files")


def sanitize_parse_args():
    parser = ArgumentParser()
    parser.add_argument("config", help="Path to config file")
    parser.add_argument(
        "--path", help="Alternate sanitization path to override the config file's path.")

    parsed = parser.parse_args()
    return parsed


def main():
    args = sanitize_parse_args()
    config_path = args.config
    config = ConfigParser()
    config.optionxform = str
    config.read(config_path)
    if args.path:
        sanitize_path = args.path
    else:
        sanitize_path = config['main']['sanitize_path']

    replacement_map = dict(config['replacements'])

    sanitize_files(sanitize_path, replacement_map)


if __name__ == "__main__":
    main()
