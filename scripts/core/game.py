
import pygame
from ..graphics.renderer import Renderer
from ..graphics.hud import HUD as hud
from .gameManager import GameManager
from .Camera import Camera
from .InputHandler import InputHandler
from ..Menus.BaseMenu.Menu import Menu
from ..Menus.GameScreen.Game import GameMenu
from ..Menus.MainMenuScreen.MainMenu import MainMenu
from ..Menus.GameSettingsScreen.GameSettings import GameSettingsMenu
from ..utils.EventManager import EventManager, event_manager
from .Enums import Events

class Game:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 1000

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.clock = pygame.time.Clock()

        game_file = None

        self.menus = {
            "main": MainMenu(self),
            "game_settings" : GameSettingsMenu(self),
            "game": GameMenu(self),
        }
        self.current_menu = self.menus["main"]
        self.camera = self.menus["game"].camera
        self.renderer = Renderer(self.screen,camera=self.camera)
        self.input_handler = InputHandler(self)
        self.hud = hud(self.screen)

        


    def event_loop(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        self.input_handler.handle_events(events)


    def update(self):
        self.event_loop()
        self.input_handler.handle_keys()
        self.current_menu.update(self.input_handler.actions_pressed)
        # self.game_manager.update()
        self.renderer.render(self)
        self.hud.update(self.current_menu, self.current_menu.objects, self.input_handler.actions_pressed, self.camera)
        self.clock.tick(60)  # Limit to 60 FPS

    def quit(self):
        self.running = False


    def initialize_game_manager(self, game_manager):
        self.menus["game"].game_manager = game_manager