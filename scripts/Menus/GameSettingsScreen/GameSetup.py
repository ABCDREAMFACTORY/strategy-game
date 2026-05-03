import random
from enum import Enum
from ...core.Enums import ResourceType
from ...core.Player import Player
from ...core.gameManager import GameManager
from ...core.Position import Position
from ...core.Tile import Tile
from ...core.GameData import GameData, game_data
from ...map.Map import Map

from typing import TYPE_CHECKING, cast
if TYPE_CHECKING:
    from ...core.game import Game
    from ..GameScreen.Game import GameMenu

class PlayerSetup:
    def __init__(self, game: "Game", name: str, civ_name: str) -> None:
        self.game = game
        self.name = name
        self.civ_name = civ_name
        self.start_pos:Position|None = None

    def __repr__(self) -> str:
        return f"PlayerSetup(name={self.name}, civ_name={self.civ_name}, start_pos={self.start_pos})"


class GameSetup:
    class MapType(Enum):
        DEFAULT = "default"
        RANDOM = "random"
        ISLAND = "island"
    class MAP_SIZE(Enum):
        TINY = (20, 20)
        SMALL = (50, 50)
        MEDIUM = (100, 100)
        LARGE = (200, 200)
    
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.players: list[PlayerSetup] = [PlayerSetup(game=game, name="Player 1", civ_name="Random"), PlayerSetup(game=game, name="Player 2", civ_name="Random")]
        self.map_type: GameSetup.MapType = GameSetup.MapType.DEFAULT
        self.map_size: GameSetup.MAP_SIZE = GameSetup.MAP_SIZE.SMALL
        self.map_setup: MapSetup = MapSetup(self)

    def add_player(self, name: str, civ_name: str):
        new_player = PlayerSetup(game=self.game, name=name, civ_name=civ_name)
        self.players.append(new_player)
            

class TileSetup:
    def __init__(self, terrain: str, resource: ResourceType):
        self.terrain = terrain
        self.resource = resource
        self.owner:"PlayerSetup|None" = None
        self.city = None
    def get_neighbors(self, pos: Position, map: "MapSetup") -> list["TileSetup"]:
        neighbors:list[TileSetup] = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                neighbor_x = pos.x + dx
                neighbor_y = pos.y + dy
                if 0 <= neighbor_x < map.width and 0 <= neighbor_y < map.height:
                    neighbors.append(map.tiles[neighbor_y][neighbor_x])
        return neighbors
    
    def to_tile(self) -> Tile:
        return Tile(terrain=self.terrain, resource=self.resource, owner=None, city=None)

class MapSetup:
    def __init__(self, game_setup: GameSetup):
        self.game_setup = game_setup
        self.width, self.height = game_setup.map_size.value
        self.tiles: list[list[TileSetup]] = self.generate_map()
    def get_tile(self, pos: Position) -> TileSetup:
        tile = self.tiles[pos.y][pos.x]
        if tile is None:
            raise ValueError(f"Tile at position {pos} has not been generated yet")
        return tile
    
    def generate_map(self) -> list[list[TileSetup]]:
        tiles:list[list[TileSetup]] = [[TileSetup("grass", ResourceType.GOLD) for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                terrain = random.choice(list(game_data.data_terrains.keys()))
                resource = random.choice(list(ResourceType))
                tiles[y][x] = TileSetup(terrain=terrain, resource=resource)
        return tiles
    
    def to_map(self) -> "Map":
        return Map(width=self.width, height=self.height, tiles=[[tile.to_tile() for tile in row] for row in self.tiles])
        
class GameManagerInitializer:
    def __init__(self, game: "Game", game_setup: GameSetup):
        self.game = game
        self.game_setup = game_setup
        self.game_menu = self.game.menus.get("game")
        self.map = self.game_setup.map_setup.to_map()

    def choose_spawn_positions(self) -> None:
        # This function should assign a start position to each player if not already assigned
        # For simplicity, we will just assign them in a line with a gap of 3 tiles
        for i, player in enumerate(self.game_setup.players):
            pos = Position(random.randint(0, self.game_setup.map_setup.width-2), random.randint(0, self.game_setup.map_setup.height-2))
            while not self.is_free_city_position(pos):
                pos = Position(random.randint(0, self.game_setup.map_setup.width-2), random.randint(0, self.game_setup.map_setup.height-2))
            player.start_pos = pos
            self.game_setup.map_setup.get_tile(pos).owner = player
            for tile in self.game_setup.map_setup.get_tile(pos).get_neighbors(pos, self.game_setup.map_setup):
                tile.owner = player
                
    def is_free_city_position(self, pos: Position) -> bool:
        tile = self.game_setup.map_setup.get_tile(pos)  # This will raise an error if the position is not valid
        if tile.owner is not None:
            return False
        for itile in tile.get_neighbors(pos, self.game_setup.map_setup):
            if itile.owner is not None:
                return False
        return True
    
    def choose_random_civilizations(self) -> None:
        civilizations = list(GameData().data_civilizations.keys())
        for player in self.game_setup.players:
            if player.civ_name == "Random":
                player.civ_name = random.choice(civilizations)
                civilizations.remove(player.civ_name)
   
    def initialize_game_manager(self) -> GameManager:
        self.choose_spawn_positions()
        self.choose_random_civilizations()
        players = [Player(self.map, ps.name, ps.civ_name, ps.start_pos) for ps in self.game_setup.players if ps.start_pos is not None]
        width, height = self.game_setup.map_size.value
        return GameManager(self.game, players, self.map, map_width=width, map_height=height)

    