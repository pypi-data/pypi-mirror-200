from typing import Any
from .object import Object


class Result(Object):
    def __init__(self, success: bool = False, msg: str = None, data: Any = None, wait: int = 5, **kwargs) -> None:
        self.success = success
        self.msg = msg or ''
        self.data = data
        self.wait = wait or 0
