from __future__ import annotations

import json
import pygame
from typing import TYPE_CHECKING, cast, Any

from ..graphics.hud import HUDElement, Button, ListSelector
from ..core.Enums import ActionType
from ..Menus.GameSettingsScreen.GameSetup import PlayerSetup

if TYPE_CHECKING:
    from ..Menus.BaseMenu.Menu import Menu
    from ..core.Player import Player
    from ..core.game import Game

class Popup:
    def __init__(self, game: Game, menu: Menu, name: str, objects: list[HUDElement] | None = None):
        self.game: Game = game
        self.menu: Menu = menu
        self.name: str = name
        self.objects: list[HUDElement] = objects or []
        self.overlay: pygame.Surface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 200))  # Semi-transparent black


    def render(self, screen: pygame.Surface, font: pygame.font.Font, camera: object) -> None:
        screen.blit(self.overlay, (0, 0))
        for obj in self.objects:
            obj.render(screen, font, camera)

    def update(self, actions_pressed: set[ActionType]) -> None:
        for obj in self.objects:
            obj.update(actions_pressed, camera=self.game.camera)

    def on_click(self, mouse_pos: tuple[int, int], camera: object) -> None:
        for obj in self.objects:
            obj.on_click(mouse_pos, camera)

    def getObjectById(self, id: str | int) -> HUDElement | None:
        for obj in self.objects:
            if obj.id == id:
                return obj
        return None
    
    def get_menu(self, menu_name: str) -> Menu:
        if menu_name not in self.game.menus:
            raise ValueError(f"Menu '{menu_name}' not found!")
        return self.game.menus[menu_name]
    
    def close(self) -> None:
        self.menu.current_popup = None

class CivilizationSelectorPopup(Popup):
    def __init__(self, game: Game, menu: Menu, player_selected: PlayerSetup | None):
        self.game: Game = game
        self.menu: Menu = menu
        typed_menu = cast(Any, self.menu)
        if not hasattr(typed_menu, "get_available_civilizations"):
            raise TypeError("Civilization selector popup requires a game settings menu")

        available_civilizations = cast(list[str], typed_menu.get_available_civilizations())
        objects = [
            ListSelector(id="civselector", x=500, y=300, width=200, height=50, text="Select Civilization", options=["Random"] + available_civilizations, on_click=self.on_civilization_selected),
            Button(id=1, x=700, y=200, width=100, height=50, text="Close", func=self.close)
        ]

        super().__init__(game, menu=menu, name="civselector", objects=objects)

        self.player_selected = player_selected

    def on_civilization_selected(self) -> None:
        civ_selector = self.getObjectById("civselector")
        if not isinstance(civ_selector, ListSelector):
            return

        civilization = civ_selector.get_value()
        civ_selector.selected_index = None

        # Handle the logic when a civilization is selected
        print(f"Civilization selected: {civilization}")
        
        if self.player_selected is not None and civilization is not None:
            self.player_selected.civ_name = civilization

        self.player_selected = None

        typed_menu = cast(Any, self.menu)
        if hasattr(typed_menu, "get_players_labels"):
            parent_selector = self.menu.getObjectById("civselector")
            if isinstance(parent_selector, ListSelector):
                parent_selector.new_list(cast(list[str], typed_menu.get_players_labels()))

        self.close()

    def get_civilizations(self) -> list[str]:
        with open("data/config/civilisation.json", "r") as f:
            civilizations = list(json.load(f).keys())
        return civilizations