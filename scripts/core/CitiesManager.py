from __future__ import annotations

from typing import TYPE_CHECKING

from ..utils.EventManager import event_manager
from ..core.Enums import Events

if TYPE_CHECKING:
    from .game import Game
    from .Civ import Civilisation
    from .City import City
    from ..map.Map import Map
    from .Position import Position

class CitiesManager:
    def __init__(self, civ:Civilisation, map:Map) -> None:
        self.civ = civ
        self.cities: list[City] = []
        self.map = map

    def add_city(self, city: City) -> None:
        for tile_pos in self.map.get_tiles_in_radius((city.pos.x, city.pos.y), radius=1):
            owner = self.map.get_tile(tile_pos).owner
            if owner is not None:
                raise ValueError(f"Cannot found city '{city.name}' at position {city.pos} because tile at {tile_pos} is already owned by civilisation {owner.civ_name}")

        self.cities.append(city)
        event_manager.notify(Events.FOUNDED_CITY, data=city)

        for tile_pos in self.map.get_tiles_in_radius((city.pos.x, city.pos.y), radius=1):
            self.add_territory(tile_pos)
        self.map.get_tile((city.pos.x, city.pos.y)).city = city

    def add_territory(self, pos: tuple[int, int]) -> None:
        self.map.get_tile(pos).owner = self.civ.player

    def find_random_city_emplacement(self) -> Position:
        for y in range(self.map.height):
            for x in range(self.map.width):
                can_found = True
                tile = self.map.get_tile((x, y))
                for tile_pos in self.map.get_tiles_in_radius((x, y), radius=1):
                    owner = self.map.get_tile(tile_pos).owner
                    if owner is not None:
                        can_found = False
                        break
                if can_found and tile.terrain != "water" and tile.owner is None:
                    return Position(x, y)
        raise ValueError("No valid city placement found")