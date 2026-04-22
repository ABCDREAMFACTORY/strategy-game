from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from ...graphics.hud import HUDElement
from ...core.Enums import ActionType

if TYPE_CHECKING:
    from ...core.Camera import Camera
    from ...core.game import Game

if TYPE_CHECKING:
    import pygame
    from ...Popups.Popup import Popup
    from ...core.game import Game

class Menu:
    def __init__(self, game: Game, name: str, objects: Sequence[HUDElement], background: pygame.Surface | None = None):
        self.game: Game = game
        self.name: str = name
        self.objects: list[HUDElement] = list(objects)
        self.background: pygame.Surface | None = background
        self.current_popup: Popup | None = None

    def render(self, screen: pygame.Surface, font: pygame.font.Font, camera: Camera) -> None:
        for obj in self.objects:
            obj.render(screen, font, camera)
        if self.current_popup is not None:
            self.current_popup.render(screen, font, camera)

    def get_menu(self, menu_name: str) -> Menu:
        if menu_name not in self.game.menus:
            raise ValueError(f"Menu '{menu_name}' not found!")
        return self.game.menus[menu_name]

    def reset(self) -> None:
        self.current_popup = None
    
    def change_menu(self, menu_name: str) -> None:
        if menu_name in self.game.menus:
            self.reset()
            self.game.current_menu = self.game.menus[menu_name]
            self.game.current_menu.sort()
        else:
            raise ValueError(f"Menu '{menu_name}' not found!")
        
    def update(self, actions_pressed: set[ActionType]) -> None:
        if self.current_popup is not None:
            self.current_popup.update(actions_pressed)

    def getObjectById(self, id: str | int) -> HUDElement | None:
        for obj in self.objects:
            if obj.id == id:
                return obj
        return None
    
    def get_popup(self) -> Popup | None:
        return self.current_popup
    
    def add_object(self, obj: HUDElement) -> None:
        self.objects.append(obj)
        self.sort()
        
    def sort(self) -> None:
        self.objects.sort(key=lambda o: o.layer, reverse=True)