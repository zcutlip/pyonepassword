from pathlib import Path
from pyonepassword import OPServerItem
import json

from _util.functions import snippet_dir, scratch_dir

server_json = Path(snippet_dir(), "server.json")
server_dict = json.load(open(server_json, "r"))
server = OPServerItem(server_dict)


def dump_server():
    out_path = Path(scratch_dir(), "modified-server.json")
    json.dump(server._item_dict, open(out_path, "w"), indent=2)
