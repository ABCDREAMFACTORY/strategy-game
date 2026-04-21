from __future__ import annotations

from typing import TYPE_CHECKING

from .Civ import Civilisation

if TYPE_CHECKING:
    from .Position import Position
    from .game import Game
    from .gameManager import GameManager

class Player:
    def __init__(self, game: Game, name: str, civ_name: str, start_position: Position) -> None:
        self.game: Game = game
        self.name: str = name
        self.civ_name: str = civ_name
        self.start_position: Position = start_position
        self.civ: Civilisation | None = None

    def initialize_civilisation(self, game_manager: GameManager) -> None:
        self.civ = Civilisation(game_manager, self.civ_name, self.start_position)