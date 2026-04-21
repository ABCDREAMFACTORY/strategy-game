from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from .City import City
from .Position import Position
from ..utils.EventManager import event_manager
from ..core.Enums import Events

if TYPE_CHECKING:
    from .gameManager import GameManager

class Civilisation:
    def __init__(self, game_manager: GameManager, name: str, start_position: Position, is_player: bool = True) -> None:
        if game_manager is None:
            raise ValueError("game_manager must be initialized before creating a Civilisation")
        self.game: GameManager = game_manager
        self.name: str = name
        data = self.get_data()
        self.color: Any = data["color"]
        self.cities: list[City] = []
        self.add_city(name=data["cities"][0],pos=start_position)
        self.is_player: bool = is_player
    
    def add_city(self, name: str, pos: Position | tuple[int, int]) -> None:
        for tile_pos in self.game.map.get_tiles_in_radius(self._to_map_coords(pos), radius=1):
            if self.game.map.get_tile(self._to_map_coords(tile_pos)).owner is not None:
                raise ValueError(f"Cannot found city '{name}' at position {pos} because tile at {tile_pos} is already owned by another civilisation")

        self.cities.append(City(name, pos))
        self.game.map.get_tile(self._to_map_coords(pos)).city = self.cities[-1]
        for tile_pos in self.game.map.get_tiles_in_radius(self._to_map_coords(pos), radius=1):
            self.game.map.get_tile(self._to_map_coords(tile_pos)).owner = self

        event_manager.notify(Events.FOUNDED_CITY, data=self.cities[-1])

    def _to_map_coords(self, pos: Position | tuple[int, int]) -> tuple[int, int]:
        if isinstance(pos, Position):
            return (pos.x, pos.y)
        return (pos[0], pos[1])
    
    def get_data(self) -> dict[str, Any]:
        with open("data/config/civilisation.json","r",encoding="utf-8") as f:
            data = json.load(f)[self.name]
        return data