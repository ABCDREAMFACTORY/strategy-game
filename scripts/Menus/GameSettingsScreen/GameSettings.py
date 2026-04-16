from ..BaseMenu.Menu import Menu
from ...graphics.hud import Button, IntSelector
from ...core.Player import Player
from ...core.Position import Position
from ...core.gameManager import GameManager

class GameSettingsMenu(Menu):
    def __init__(self, game):
        self.game = game
        objects = [
            IntSelector(id="nbplayers", x=500, y=300, width=200, height=50, text="Number of players", value=2, min_value=2, max_value=100),
            Button(id=1,x=500, y=400, width=200, height=50, text="Start game", func=lambda:self.start_new_game()),
            Button(id=2,x=500, y=470, width=200, height=50, text="Back to main menu", func=lambda: self.change_menu("main")),
        ]
        super().__init__(game, "settings", objects)

    def start_new_game(self):
        nbplayers_selector = self.getObjectById("nbplayers")
        if nbplayers_selector is None:
            raise ValueError("Number of players selector not found!")
        players = []
        for iplayer in range(nbplayers_selector.value):
            players.append(Player(self.game, civ_name="France", start_position=Position(3*iplayer,0)))
            

        self.game.initialize_game_manager(GameManager(
            self.game,
            players,
            map_width=50,
            map_height=50
        ))
        self.change_menu("game")
