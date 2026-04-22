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

class Player:
    def __init__(self, game: Game, name: str, civ_name: str, start_position: Position) -> None:
        self.game: Game = game
        self.name: str = name
        self.civ_name: str = civ_name
        self.start_position: Position = start_position
        self.civ: Civilisation | None = None
        event_manager.subscribe(Events.GAME_MANAGER_INITIALIZED, self.initialize_civilisation)

    def initialize_civilisation(self, game_manager:"GameManager") -> None:
        if game_manager is None:
            raise ValueError("Game manager is not initialized yet")
        # A Player should initialize exactly once per game creation.
        # Unsubscribing avoids stale Players from previous sessions reacting
        # when a new game is started from the menu.
        event_manager.unsubscribe(Events.GAME_MANAGER_INITIALIZED, self.initialize_civilisation)
        if self.civ is not None:
            return
        self.civ = Civilisation(self, game_manager, self.civ_name, self.start_position)