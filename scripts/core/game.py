
from __future__ import annotations

import pygame
from typing import TYPE_CHECKING, cast

from ..graphics.renderer import Renderer
from ..graphics.hud import HUD as hud
from .InputHandler import InputHandler
from ..Menus.GameScreen.Game import GameMenu
from ..Menus.MainMenuScreen.MainMenu import MainMenu
from ..Menus.GameSettingsScreen.GameSettings import GameSettingsMenu

if TYPE_CHECKING:
    from ..Menus.BaseMenu.Menu import Menu
    from .Camera import Camera

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.width: int = 1200
        self.height: int = 1000

        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()

        game_file = None

        self.menus: dict[str, Menu] = {
            "main": MainMenu(self),
            "game_settings" : GameSettingsMenu(self),
            "game": GameMenu(self),
        }
        self.current_menu: Menu = self.menus["main"]
        game_menu = cast(GameMenu, self.menus["game"])
        self.camera: Camera = game_menu.camera
        self.renderer: Renderer = Renderer(self.screen,camera=self.camera)
        self.input_handler: InputHandler = InputHandler(self)
        self.hud: hud = hud(self.screen)

        


    def event_loop(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        self.input_handler.handle_events(events)


    def update(self) -> None:
        self.event_loop()
        self.input_handler.handle_keys()
        self.current_menu.update(self.input_handler.actions_pressed)
        # self.game_manager.update()
        self.renderer.render(self)
        self.hud.update(self.current_menu, self.current_menu.objects, self.input_handler.actions_pressed, self.camera)
        self.clock.tick(60)  # Limit to 60 FPS

    def quit(self) -> None:
        self.running = False