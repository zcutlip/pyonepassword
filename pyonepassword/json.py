import json


def safe_unjson(json_or_obj):
    """
    Transparently un-json things if they are strings, and no-op if not
    """
    if isinstance(json_or_obj, str):
        obj = json.loads(json_or_obj)
    else:
        obj = json_or_obj
    return obj
