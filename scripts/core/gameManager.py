import gzip
import json
from pathlib import Path
from ..utils.SaveManager import SaveManager
from ..map.Map import Map
from .Enums import Events
from ..utils.EventManager import event_manager



class GameManager:
    def __init__(self, game, players, game_file: Path | str | None = None, map_width=10, map_height=10):
        self.game = game
        self.save_manager = SaveManager(game)
        self.width = map_width
        self.height = map_height
        self.current_turn = 0
        self.players = players
        self.map = Map.new_map(map_width, map_height)

        for player in self.players:
            player.initialize_civilisation(self)

        if game_file:
            self.save_manager.load_game(game_file)



        event_manager.notify(Events.GAME_MANAGER_INITIALIZED, data=self)

    def to_dict(self) -> dict:
        return {
            "version": 1,
            "current_turn": self.current_turn,
            "players": self.players,
            "map": self.map.to_dict(compact=True),
        }


