from __future__ import annotations

import random
import json
from typing import TYPE_CHECKING, cast

from ..BaseMenu.Menu import Menu
from ...graphics.hud import Button, IntSelector, ListSelector
from ...core.Player import Player
from ...core.Position import Position
from ...core.gameManager import GameManager
from ...Popups.Popup import CivilizationSelectorPopup

if TYPE_CHECKING:
    from ...core.game import Game
    from ..GameScreen.Game import GameMenu

class GameSettingsMenu(Menu):
    def __init__(self, game: Game):
        self.game: Game = game
        self.nb_players: int = 2
        self.players: list[Player] = self.initialize_players()
        objects: list[Button | IntSelector | ListSelector] = [
            IntSelector(id="nbplayers", x=500, y=300, width=200, height=50, text="Number of players", value=2, min_value=2, max_value=len(self.get_civilizations()), on_click=self.on_nb_players_change),
            Button(id=1,x=500, y=400, width=200, height=50, text="Start game", func=lambda:self.start_new_game()),
            Button(id=2,x=500, y=470, width=200, height=50, text="Back to main menu", func=lambda: self.change_menu("main")),
            ListSelector(id="civselector", x=900, y=230, width=200, height=50, text="Joueurs", options=self.get_players_labels(), on_click=self.on_civ_selector_click)
        ]
        super().__init__(game, name="settings", objects=objects)

    def reset(self) -> None:
        self.current_popup = None
        self.nb_players = 2
        self.players = self.initialize_players()

        nbplayers_selector = self.getObjectById("nbplayers")
        if isinstance(nbplayers_selector, IntSelector):
            nbplayers_selector.value = self.nb_players
            nbplayers_selector.value_label.text = str(self.nb_players)

        civ_selector = self.getObjectById("civselector")
        if isinstance(civ_selector, ListSelector):
            civ_selector.new_list(self.get_players_labels())

    def start_new_game(self) -> None:
        nbplayers_selector = self.getObjectById("nbplayers")
        if not isinstance(nbplayers_selector, IntSelector):
            raise ValueError("Number of players selector not found!")
        

        self.choose_random_civilizations()

        GameManager(
            self.game,
            self.players,
            map_width=50,
            map_height=50
        )

        # game_menu = self.game.menus["game"]
        # game_menu.reset_session()
        # game_menu.game_manager = game_manager
        self.change_menu("game")
        self.reset()

    def on_nb_players_change(self) -> None:
        nb = self.nb_players
        nbplayers_selector = self.getObjectById("nbplayers")
        if not isinstance(nbplayers_selector, IntSelector):
            return

        self.nb_players = nbplayers_selector.value
        if nb < self.nb_players:
            self.add_player()
        elif nb > self.nb_players:
            self.players.remove(self.players[-1])
        

        civ_selector = self.getObjectById("civselector")
        if isinstance(civ_selector, ListSelector):
            civ_selector.new_list([f"{player.name}-{player.civ_name}" for player in self.players])
    
    def add_player(self) -> None:
        new_player = Player(self.game, name=f"player{self.nb_players}", civ_name="Random", start_position=Position(3*len(self.players),0))
        self.players.append(new_player)

    def on_civ_selector_click(self) -> None:
        civ_selector = self.getObjectById("civselector")
        if not isinstance(civ_selector, ListSelector) or civ_selector.selected_index is None:
            return

        player_selected = self.players[civ_selector.selected_index]
        self.current_popup = CivilizationSelectorPopup(self.game, self, player_selected)


    def get_available_civilizations(self) -> list[str]:
        civilizations = self.get_civilizations()
        used_civilizations = [player.civ_name for player in self.players]
        available_civilizations = [civ for civ in civilizations if civ not in used_civilizations]
        return available_civilizations

    def get_random_civilization(self) -> list[Player]:
        civilizations = self.get_civilizations()
        civilizations = random.sample(civilizations, self.nb_players)
        random.shuffle(civilizations)
        return [Player(self.game, name=f"player{iplayer+1}", civ_name=civilization, start_position=Position(3*iplayer,0)) for iplayer, civilization in enumerate(civilizations)]
    
    def get_civilizations(self) -> list[str]:
        with open("data/config/civilisation.json", "r") as f:
            civilizations = list(json.load(f).keys())
        return civilizations
    
    def initialize_players(self) -> list[Player]:
        return [Player(self.game, name=f"player{iplayer+1}", civ_name="Random", start_position=Position(3*iplayer,0)) for iplayer in range(self.nb_players)]
    
    def choose_random_civilizations(self) -> None:
        civilizations = self.get_civilizations()
        for player in self.players:
            if player.civ_name == "Random":
                player.civ_name = random.choice(civilizations)
                civilizations.remove(player.civ_name)

    def get_players_labels(self) -> list[str]:
        return [f"{player.name}-{player.civ_name}" for player in self.players]