from dataclasses import dataclass
from datetime import datetime

__all__ = [
    "BaseModel"
]

@dataclass
class BaseModel:
    @classmethod
    def from_json(cls, obj):
        raise NotImplementedError()

    @staticmethod
    def _from_props(cls, obj: dict, fieldstr: str):
        return cls(*BaseModel._unpack_props(obj, fieldstr))

    @staticmethod
    def _unpack_props(obj: dict, fieldstr: str):
        items = [obj.get(f, None) for f in fieldstr.split(" ")]
        return items

    @staticmethod
    def _unpack_list(cls, lst: list):
        return [cls.from_json(x) for x in lst]

    @staticmethod
    def _datetime(dt):
        if dt is None:
            return dt

        return datetime.fromtimestamp(int(dt))