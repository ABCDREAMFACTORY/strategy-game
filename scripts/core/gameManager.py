from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..utils.SaveManager import SaveManager
from ..map.Map import Map
from .Enums import Events, Mode
from ..utils.EventManager import event_manager
from .Tile import Tile

if TYPE_CHECKING:
    from .Player import Player
    from .game import Game


class GameManager:
    def __init__(
        self,
        game: Game,
        players: list[Player],
        map: Map,
        game_file: Path | str | None = None,
        map_width: int = 10,
        map_height: int = 10, 
        mode: Mode = Mode.SINGLE_PLAYER_LOCAL
    ):
        self.game: Game = game
        self.save_manager: SaveManager = SaveManager(game)
        self.width: int = map_width
        self.height: int = map_height
        self.current_turn: int = 0
        self.players: list[Player] = players
        self.map: Map = map
        self.mode = mode
        self.actual_player: Player = self.players[0]


        if game_file:
            self.save_manager.load_game(game_file)


        print([player.civ_name for player in self.players])

        event_manager.subscribe(Events.TILE_CLICKED, self.on_tile_clicked)


    def update(self) -> None:
        if self.mode == Mode.SINGLE_PLAYER_AI:
            self.single_player_ai_update()
        elif self.mode == Mode.SINGLE_PLAYER_LOCAL:
            self.single_player_local_update()
        elif self.mode == Mode.MULTIPLAYER:
            self.multiplayer_update()

    def single_player_local_update(self) -> None:
        pass


    def single_player_ai_update(self) -> None:
        pass


    def multiplayer_update(self) -> None:
        pass

    def on_tile_clicked(self, tile: Tile) -> None:
        print(f"Tile clicked: {tile.pos}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": 1,
            "current_turn": self.current_turn,
            "players": self.players,
            "map": self.map.to_dict(compact=True),
        }


