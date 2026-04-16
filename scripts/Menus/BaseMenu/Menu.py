from ...core.gameManager import GameManager
from ...graphics.hud import Button, IntSelector, CityNameLabel
from ...core.Camera import Camera
from ...core.Player import Player
from ...core.Position import Position
from ...graphics.AssetsManager import AssetsManager
from ...utils.EventManager import EventManager, event_manager
from ...core.Enums import Events

class Menu:
    def __init__(self, game, name, objects, background = None):
        self.game = game
        self.name = name
        self.objects = objects
        self.background = background
    def render(self, screen, font, camera):
        for obj in self.objects:
            obj.render(screen, font, camera)
    def get_menu(self, menu_name):
        if menu_name not in self.game.menus:
            raise ValueError(f"Menu '{menu_name}' not found!")
        return self.game.menus.get(menu_name)
    def change_menu(self, menu_name):
        if menu_name in self.game.menus:
            self.game.current_menu = self.game.menus[menu_name]
        else:
            raise ValueError(f"Menu '{menu_name}' not found!")
    def update(self, actions_pressed):
        pass
    def getObjectById(self, id) -> object:
        for obj in self.objects:
            if obj.id == id:
                return obj
        return None
