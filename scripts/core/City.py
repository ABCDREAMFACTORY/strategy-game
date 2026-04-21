
from __future__ import annotations

from .Position import Position


class City:
    def __init__(self, name: str, pos: Position | tuple[int, int]) -> None:
        self.name: str = name
        self.pos: Position | tuple[int, int] = pos