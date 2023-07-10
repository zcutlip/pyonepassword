#!/usr/bin/env python3

import fnmatch
import hashlib
import json
import os
import re
import shutil
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path
from typing import Dict

WHITELIST = ["*/output", "*.txt", "*.json", "*.py", "*/input/**"]


def digest_file(file_path):
    data = open(file_path, "rb").read()
    digest = None
    # ignore input if None or if empty string
    if data:
        if isinstance(data, str):
            data = data.encode()
        hash = hashlib.md5(data)
        digest = hash.hexdigest()
    return digest


class InputHashes:
    """
    A class to track changes to input data to 'mock-op' so that response
    directories can be updated allowing responses to be looked up by
    the input's new hash

    This addresses the problem where this script santizes mock-op output that
    would later be used as input to another mock-op invocation.

    If the previous command's output has changed the hash of the next command's
    input will have changed as well, and can't be located in the response
    directory by its hash
    """
    INPUT_FILE_BASENAME = "input.bin"

    def __init__(self):
        self._input_paths = {}
        self._updated_hashes = {}

    def add_input_path(self, input_path):
        input_path = Path(input_path)
        if input_path.name == self.INPUT_FILE_BASENAME:
            original_hash = digest_file(input_path)
            parent_base = input_path.parent.name
            if parent_base == original_hash:
                print(
                    f"Adding input file: {input_path}, hash: {original_hash}")
                self._input_paths[input_path] = {"orig_hash": original_hash}

    def update_input_paths(self):
        for key, pathdict in self._input_paths.items():
            input_path = Path(key)
            file_base = input_path.name
            parent = input_path.parent
            parent_base = input_path.parent.name
            containing_path = parent.parent

            orig_hash = pathdict["orig_hash"]
            if orig_hash != parent_base:
                continue

            new_hash = digest_file(input_path)
            if new_hash == orig_hash:
                continue
            new_path = Path(containing_path, new_hash, file_base)
            new_parent = new_path.parent
            new_parent.mkdir(parents=True, exist_ok=True)
            print(f"moving: {input_path}")
            print(f"to: {new_path}")
            shutil.move(input_path, new_path)
            parent.rmdir()

            self._updated_hashes[orig_hash] = new_hash

    @property
    def updated_hashes(self) -> Dict[str, str]:
        return self._updated_hashes


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
            print(f"Sanitized {self._fpath}")
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


def _santize_single(filepath, sanitization_map, whitelist, input_hashes=None):
    changed = False
    considered = False
    for pattern in whitelist:
        if fnmatch.fnmatch(filepath, pattern):

            if filepath.suffix == ".json":
                textfile = JSONFile(filepath, sanitization_map)
            else:
                textfile = TextFile(filepath, sanitization_map)
            considered = True
            if input_hashes:
                input_hashes.add_input_path(filepath)
            changed = textfile.sanitize()
            break
    return (considered, changed)


def sanitize_files(sanitize_path, sanitization_map, input_hashes=None):
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
                    filepath, sanitization_map, local_whitelist, input_hashes=input_hashes)
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
    print(f"Sanitizing: {sanitize_path}")
    replacement_map = dict(config['replacements'])

    input_hashes = InputHashes()
    sanitize_files(sanitize_path, replacement_map, input_hashes=input_hashes)

    # calculate new hashes of all 'input.bin' files and move them to their new directories
    # and track all old_hash:new_hash pairs in a dictionary
    input_hashes.update_input_paths()

    # Run the sanitization again, this time with the {old_hash:new_hash}
    # map for any changed input files
    # If any changed, this should result in the corresponding response directory JSON
    # files being updated accordingly.
    sanitize_files(sanitize_path, input_hashes.updated_hashes)


if __name__ == "__main__":
    main()
