from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..utils.SaveManager import SaveManager
from ..map.Map import Map
from .Enums import Events
from ..utils.EventManager import event_manager

if TYPE_CHECKING:
    from .Player import Player
    from .game import Game


class GameManager:
    def __init__(
        self,
        game: Game,
        players: list[Player],
        game_file: Path | str | None = None,
        map_width: int = 10,
        map_height: int = 10,
    ):
        self.game: Game = game
        self.save_manager: SaveManager = SaveManager(game)
        self.width: int = map_width
        self.height: int = map_height
        self.current_turn: int = 0
        self.players: list[Player] = players
        self.map: Map = Map.new_map(map_width, map_height)

        for player in self.players:
            player.initialize_civilisation(self)

        if game_file:
            self.save_manager.load_game(game_file)


        print([player.civ_name for player in self.players])
        event_manager.notify(Events.GAME_MANAGER_INITIALIZED, data=self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": 1,
            "current_turn": self.current_turn,
            "players": self.players,
            "map": self.map.to_dict(compact=True),
        }


