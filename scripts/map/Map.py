from __future__ import annotations

import gzip
import json
from random import choice
from typing import Any

from ..core.GameData import game_data
from ..core.Enums import ResourceType
from ..core.Tile import Tile
from ..core.Position import Position


class Map:
    def __init__(self, width: int, height: int, tiles: list[list[Tile]]):
        self.width: int = width
        self.height: int = height
        self.tiles: list[list[Tile]] = tiles

    def get_tile(self, pos: tuple[int, int]) -> Tile:
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        else:
            raise IndexError(f"Position {pos} is out of bounds for map of size {self.width}x{self.height}")

    def get_tiles_in_radius(self, center_pos: tuple[int, int], radius: int) -> list[tuple[int, int]]:
        cx, cy = center_pos
        tiles_in_radius = []
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    tiles_in_radius.append((x, y))
        return tiles_in_radius
    
    
    
    def to_dict(self, compact: bool = True) -> dict[str, Any]:
        if compact:
            return {
                "format": "compact-v1",
                "width": self.width,
                "height": self.height,
                "tiles": [
                    [
                        [
                            tile.terrain,
                            tile.resource.value,
                            tile.unit,  #Problème: unit est une classe
                            tile.city,
                            int(tile.visible),
                            int(tile.explored),
                        ]
                        for tile in row
                    ]
                    for row in self.tiles
                ],
            }

        return {
            "width": self.width,
            "height": self.height,
            "tiles": [
                [
                    {
                        "terrain": tile.terrain,
                        "resource": tile.resource.value,
                        "unit": tile.unit,
                        "city": tile.city,
                        "visible": tile.visible,
                        "explored": tile.explored,
                    }
                    for tile in row
                ]
                for row in self.tiles
            ],
        }

    def save_map(self, filename: str, compact: bool = True) -> None:
        data = self.to_dict(compact=compact)

        if filename.endswith(".gz"):
            with gzip.open(filename, "wt", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
            return

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    @classmethod
    def load_map(cls, filename: str) -> Map:
        if filename.endswith(".gz"):
            with gzip.open(filename, "rt", encoding="utf-8") as f:
                data = json.load(f)
            return cls.dict_to_map(data)

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.dict_to_map(data)

    @classmethod
    def dict_to_map(cls, data: dict[str, Any]) -> Map:
        width = data["width"]
        height = data["height"]
        tiles: list[list[Tile]] = [
            [Tile("grass", ResourceType.FOOD) for _ in range(width)] for _ in range(height)
        ]

        first_tile = data["tiles"][0][0] if data.get("tiles") and data["tiles"][0] else None
        compact_format = data.get("format") == "compact-v1" or isinstance(first_tile, list)

        for j in range(height):
            for i in range(width):
                tile_data = data["tiles"][j][i]
                if compact_format:
                    terrain = tile_data[0]
                    resource = ResourceType(tile_data[1])
                    unit = tile_data[2]
                    city = tile_data[3]
                    visible = bool(tile_data[4])
                    explored = bool(tile_data[5])
                else:
                    terrain = tile_data["terrain"]
                    resource = ResourceType(tile_data["resource"])
                    unit = tile_data["unit"]
                    city = tile_data["city"]
                    visible = bool(tile_data["visible"])
                    explored = bool(tile_data["explored"])

                tiles[j][i] = Tile(
                    terrain=terrain,
                    resource=resource,
                    unit=unit,
                    city=city,
                    visible=visible,
                    explored=explored,
                )

        return cls(width=width, height=height, tiles=tiles)

    @classmethod
    def new_map(cls, width: int, height: int) -> Map:
        return cls(
            width=width,
            height=height,
            tiles=[
                [Tile(terrain=choice(list(game_data.data_terrains.keys())), resource=choice(list(ResourceType))) for _ in range(width)]
                for _ in range(height)
            ],
        )

    def __str__(self) -> str:
        return "\n".join(
            ["".join([f"{tile.terrain[0]}{tile.resource.name[0]}" for tile in row]) for row in self.tiles]
        )

