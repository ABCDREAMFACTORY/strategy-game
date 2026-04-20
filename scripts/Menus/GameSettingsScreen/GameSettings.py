import random
import json
from ..BaseMenu.Menu import Menu
from ...graphics.hud import Button, IntSelector, ListSelector
from ...core.Player import Player
from ...core.Position import Position
from ...core.gameManager import GameManager
from ...Popups.Popup import CivilizationSelectorPopup

class GameSettingsMenu(Menu):
    def __init__(self, game):
        self.game = game
        self.nb_players = 2
        self.players = self.initialize_players()
        objects = [
            IntSelector(id="nbplayers", x=500, y=300, width=200, height=50, text="Number of players", value=2, min_value=2, max_value=len(self.get_civilizations()), on_click=self.on_nb_players_change),
            Button(id=1,x=500, y=400, width=200, height=50, text="Start game", func=lambda:self.start_new_game()),
            Button(id=2,x=500, y=470, width=200, height=50, text="Back to main menu", func=lambda: self.change_menu("main")),
            ListSelector(id="civselector", x=900, y=230, width=200, height=50, text="Joueurs", options=self.get_players_labels(), on_click=self.on_civ_selector_click)
        ]
        popups = [
            CivilizationSelectorPopup(game, self)
        ]
        super().__init__(game, name="settings", objects=objects, popups=popups)

    def start_new_game(self):
        nbplayers_selector = self.getObjectById("nbplayers")
        if nbplayers_selector is None:
            raise ValueError("Number of players selector not found!")
        

        self.choose_random_civilizations()

        GameManager(
            self.game,
            self.players,
            map_width=50,
            map_height=50
        )

        self.change_menu("game")

    def on_nb_players_change(self):
        nb = self.nb_players
        self.nb_players = self.getObjectById("nbplayers").value # type: ignore
        if nb < self.nb_players:
            self.add_player()
        elif nb > self.nb_players:
            self.players.remove(self.players[-1])
        

        civ_selector = self.getObjectById("civselector")
        if civ_selector is not None:
            civ_selector.new_list([player.name for player in self.players]) # type: ignore
    
    def add_player(self):
        available_civilizations = self.get_available_civilizations()
        new_player = Player(self.game, name=f"player{self.nb_players}", civ_name=random.choice(available_civilizations), start_position=Position(3*len(self.players),0))
        self.players.append(new_player)

    def on_civ_selector_click(self):
        self.current_popup = self.get_popup("civselector")
        self.current_popup.player_selected = self.players[self.getObjectById("civselector").selected_index] # type: ignore
        if self.current_popup is not None:
            self.current_popup.show()


    def get_available_civilizations(self):
        civilizations = self.get_civilizations()
        used_civilizations = [player.civ_name for player in self.players]
        available_civilizations = [civ for civ in civilizations if civ not in used_civilizations]
        return available_civilizations

    def get_random_civilization(self) -> list[Player]:
        civilizations = self.get_civilizations()
        civilizations = random.sample(civilizations, self.nb_players)
        random.shuffle(civilizations)
        return [Player(self.game, name=f"player{iplayer+1}", civ_name=civilization, start_position=Position(3*iplayer,0)) for iplayer, civilization in enumerate(civilizations)]
    
    def get_civilizations(self):
        with open("data/config/civilisation.json", "r") as f:
            civilizations = list(json.load(f).keys())
        return civilizations
    
    def initialize_players(self):
        return [Player(self.game, name=f"player{iplayer+1}", civ_name="Random", start_position=Position(3*iplayer,0)) for iplayer in range(self.nb_players)]
    
    def choose_random_civilizations(self):
        civilizations = self.get_civilizations()
        for player in self.players:
            if player.civ_name == "Random":
                player.civ_name = random.choice(civilizations)
                civilizations.remove(player.civ_name)

    def get_players_labels(self):
        return [f"{player.name}-{player.civ_name}" for player in self.players]