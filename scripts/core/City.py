
from __future__ import annotations
from typing import TYPE_CHECKING

from .Position import Position

if TYPE_CHECKING:
    from .Player import Player

class City:
    def __init__(self, name: str, pos: Position | tuple[int, int], owner:Player) -> None:
        self.name: str = name
        self.pos: Position | tuple[int, int] = pos
        self.owner = owner