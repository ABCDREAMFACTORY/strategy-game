from ..BaseMenu.Menu import Menu
from ...graphics.hud import Button, IntSelector, ListSelector
from ...core.Player import Player
from ...core.Position import Position
from ...core.gameManager import GameManager
from ...Popups.Popup import CivilizationSelectorPopup

class GameSettingsMenu(Menu):
    def __init__(self, game):
        self.game = game
        self.players = [Player(self.game, name=f"player{iplayer}", civ_name="France", start_position=Position(3*iplayer,0)) for iplayer in range(2)]
        objects = [
            IntSelector(id="nbplayers", x=500, y=300, width=200, height=50, text="Number of players", value=2, min_value=2, max_value=100, on_click=self.on_nb_players_change),
            Button(id=1,x=500, y=400, width=200, height=50, text="Start game", func=lambda:self.start_new_game()),
            Button(id=2,x=500, y=470, width=200, height=50, text="Back to main menu", func=lambda: self.change_menu("main")),
            ListSelector(id="civselector", x=900, y=230, width=200, height=50, text="Joueurs", options=[player.name for player in self.players], on_click=self.on_civ_selector_click)
        ]
        popups = [
            CivilizationSelectorPopup(game)
        ]
        super().__init__(game, name="settings", objects=objects, popups=popups)

    def start_new_game(self):
        nbplayers_selector = self.getObjectById("nbplayers")
        if nbplayers_selector is None:
            raise ValueError("Number of players selector not found!")
        players = []
        for iplayer in range(nbplayers_selector.value): # type: ignore
            players.append(Player(self.game, name=f"player{iplayer}", civ_name="France", start_position=Position(3*iplayer,0)))
            

        GameManager(
            self.game,
            players,
            map_width=50,
            map_height=50
        )
        self.change_menu("game")

    def on_nb_players_change(self):
        self.players = [Player(self.game, name=f"player{iplayer}", civ_name="France", start_position=Position(3*iplayer,0)) for iplayer in range(self.getObjectById("nbplayers").value)] # type: ignore
        civ_selector = self.getObjectById("civselector")
        if civ_selector is not None:
            civ_selector.new_list([player.name for player in self.players]) # type: ignore

    def on_civ_selector_click(self):
        self.current_popup = self.get_popup("civselector")
        if self.current_popup is not None:
            self.current_popup.show()