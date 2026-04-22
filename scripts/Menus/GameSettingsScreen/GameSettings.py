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
from ...utils.EventManager import event_manager
from ...core.Enums import Events
from .GameSetup import GameSetup, PlayerSetup, GameManagerInitializer

if TYPE_CHECKING:
    from ...core.game import Game
    from ..GameScreen.Game import GameMenu

class GameSettingsMenu(Menu):
    def __init__(self, game: Game):
        self.game: Game = game
        self.game_setup = GameSetup(game)
        self.nb_players: int = len(self.game_setup.players)
        objects: list[Button | IntSelector | ListSelector] = [
            IntSelector(id="nbplayers", x=500, y=300, width=200, height=50, text="Number of players", value=2, min_value=2, max_value=len(self.get_civilizations()), on_click=self.on_nb_players_change),
            Button(id=1,x=500, y=400, width=200, height=50, text="Start game", func=lambda:self.start_new_game()),
            Button(id=2,x=500, y=470, width=200, height=50, text="Back to main menu", func=lambda: self.change_menu("main")),
            ListSelector(id="civselector", x=900, y=230, width=200, height=50, text="Joueurs", options=self.get_players_labels(), on_click=self.on_civ_selector_click)
        ]
        super().__init__(game, name="settings", objects=objects)

    def reset(self) -> None:
        self.game_setup = GameSetup(self.game)
        self.current_popup = None
        self.nb_players = 2

        nbplayers_selector = self.getObjectById("nbplayers")
        if isinstance(nbplayers_selector, IntSelector):
            nbplayers_selector.value = self.nb_players
            nbplayers_selector.value_label.text = str(self.nb_players)

        civ_selector = self.getObjectById("civselector")
        if isinstance(civ_selector, ListSelector):
            civ_selector.new_list(self.get_players_labels())

    def start_new_game(self) -> None:
        game_menu = cast("GameMenu", self.game.menus["game"])
        game_menu.reset_session()
        game_manager = GameManagerInitializer(self.game, self.game_setup).initialize_game_manager()
        game_menu.game_manager = game_manager
        event_manager.notify(Events.GAME_MANAGER_INITIALIZED, data=game_manager)
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
            self.game_setup.players.remove(self.game_setup.players[-1])
        

        civ_selector = self.getObjectById("civselector")
        if isinstance(civ_selector, ListSelector):
            civ_selector.new_list([f"{player.name}-{player.civ_name}" for player in self.game_setup.players])
    
    def add_player(self) -> None:
        self.game_setup.add_player(name=f"Player {len(self.game_setup.players)+1}", civ_name="Random")

    def on_civ_selector_click(self) -> None:
        civ_selector = self.getObjectById("civselector")
        if not isinstance(civ_selector, ListSelector) or civ_selector.selected_index is None:
            return

        player_selected = self.game_setup.players[civ_selector.selected_index]
        self.current_popup = CivilizationSelectorPopup(self.game, self, player_selected)

    def get_players_labels(self) -> list[str]:
        return [f"{player.name}-{player.civ_name}" for player in self.game_setup.players]
    
    def get_civilizations(self) -> list[str]:
        with open("data/config/civilisation.json", "r") as f:
            data = json.load(f)
        return list(data.keys())