from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from .City import City
from .Position import Position
from ..utils.EventManager import event_manager
from ..core.Enums import Events
from .CitiesManager import CitiesManager

if TYPE_CHECKING:
    from .gameManager import GameManager
    from .Player import Player
    from ..map.Map import Map

class Civilisation:
    def __init__(self,player:"Player", map:Map, name: str, start_position: Position, is_player: bool = True) -> None:
        self.player = player
        self.map = map
        self.name: str = name
        data = self.get_data()
        self.color: Any = data["color"]
        self.cities_manager = CitiesManager(self, map)
        first_city = City(name=data["cities"][0], pos=start_position, owner=self.player)
        self.cities_manager.add_city(first_city)
        self.is_player: bool = is_player

    def _to_map_coords(self, pos: Position | tuple[int, int]) -> tuple[int, int]:
        if isinstance(pos, Position):
            return (pos.x, pos.y)
        return (pos[0], pos[1])
    
    def get_data(self) -> dict[str, Any]:
        with open("data/config/civilisation.json","r",encoding="utf-8") as f:
            data = json.load(f)[self.name]
        return data