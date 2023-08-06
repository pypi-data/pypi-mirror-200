from typing import Match
from json import dumps
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path

class Object():
    @staticmethod
    def default(obj: "Object"):
        if isinstance(obj, bytes):
            return repr(obj)

        if isinstance(obj, Match):
            return repr(obj)

        if isinstance(obj, Enum):
            return str(obj)

        if isinstance(obj,(datetime,Decimal)):
            return str(obj)

        if isinstance(obj,Path):
            return str(obj.absolute())

        return {
            "_": obj.__class__.__name__,
            **{
                attr: getattr(obj, attr)
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
            }
        }

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Object.default, ensure_ascii=False)