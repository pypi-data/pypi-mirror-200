from utils import json_dumps


class AbstractException(Exception):
    __slots__ = ("code", "msg")

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    def __str__(self):
        return json_dumps(self.dict())

    def dict(self):
        return {"code": self.code, "msg": self.msg}


if __name__ == '__main__':
    try:
        raise AbstractException(120, "test")
    except AbstractException as e:
        print(e.dict())
