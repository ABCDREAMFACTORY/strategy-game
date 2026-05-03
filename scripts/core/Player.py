from __future__ import annotations
from typing import TYPE_CHECKING, cast

from .Civ import Civilisation
from ..utils.EventManager import event_manager
from ..core.Enums import Events

if TYPE_CHECKING:
    from .Position import Position
    from .game import Game
    from .gameManager import GameManager
    from ..Menus.GameScreen.Game import GameMenu
    from ..map.Map import Map
class Player:
    def __init__(self, map:"Map", name: str, civ_name: str, start_position: Position) -> None:
        self.map = map
        self.name: str = name
        self.civ_name: str = civ_name
        self.start_position: Position = start_position
        self.civ = Civilisation(self, map, self.civ_name, self.start_position)
