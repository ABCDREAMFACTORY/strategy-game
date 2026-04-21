from __future__ import annotations

from typing import TYPE_CHECKING

from ..BaseMenu.Menu import Menu
from ...graphics.hud import Button
from ...graphics.AssetsManager import AssetsManager

if TYPE_CHECKING:
    from ...core.game import Game

class MainMenu(Menu):
    def __init__(self, game: Game):
        objects = [
            Button(id=1,x=500, y=400, width=200, height=50, text="Start new Game", func=self.start_game),
            Button(id=2,x=500, y=470, width=200, height=50, text="Load Game", func=lambda: print("Load game functionality not implemented yet")),
            Button(id=3,x=500, y=540, width=200, height=50, text="Exit", func=game.quit),
        ]
        super().__init__(game, "main", objects, background=AssetsManager.load_image("assets/Backgrounds/mainmenu.png",game.width, game.height))

    def start_game(self) -> None:
        self.change_menu("game_settings")