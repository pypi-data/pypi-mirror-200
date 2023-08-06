import json


def json_dumps(data: dict, ensure_ascii=False, **kwargs):
    return json.dumps(data, ensure_ascii=ensure_ascii, **kwargs)
