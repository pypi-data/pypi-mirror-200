from collections import defaultdict

from pydantic import BaseModel, Field


class AbstractConfig(BaseModel):
    name: str = None
    desc: str = None
    class_name: str = None

    @property
    def id(self):
        args = [self.class_name, self.func_name, self.name, self.desc]
        return f"{self.class_name}.{self.func_name}"

    @property
    def func_name(self):
        return self.func_name

    @func_name.setter
    def func_name(self, func_name):
        self.func_name = func_name


class Global(BaseModel):
    settings: defaultdict = Field(default=defaultdict)
    registry: defaultdict = Field(default=defaultdict)


def configuration(unique_id):
    def wrapper(func):
        GLOBAL.settings[unique_id] = defaultdict

        def inner(*args, **kwargs):
            pass


GLOBAL = Global()

print(GLOBAL)
