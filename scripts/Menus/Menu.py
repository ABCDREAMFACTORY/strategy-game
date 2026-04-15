from ..core.gameManager import GameManager
from ..graphics.hud import Button, IntSelector, CityNameLabel
from ..core.Camera import Camera
from ..core.Player import Player
from ..core.Position import Position
from ..graphics.AssetsManager import AssetsManager

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
    def getObjectById(self, id):
        for obj in self.objects:
            if obj.id == id:
                return obj
        return None


class MainMenu(Menu):
    def __init__(self, game):
        objects = [
            Button(id=1,x=500, y=400, width=200, height=50, text="Start new Game", func=self.start_game),
            Button(id=2,x=500, y=470, width=200, height=50, text="Load Game", func=lambda: print("Load game functionality not implemented yet")),
            Button(id=3,x=500, y=540, width=200, height=50, text="Exit", func=game.quit),
        ]
        super().__init__(game, "main", objects, background=AssetsManager.load_image("assets/Backgrounds/mainmenu.png",game.width, game.height))

    def start_game(self):
        self.change_menu("game_settings")
        

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
            

        self.game.game_manager = GameManager(
            self.game,
            players,
            map_width=50,
            map_height=50
        )
        self.change_menu("game")

class GameMenu(Menu):
    def __init__(self, game):
        self.game = game
        objects = [
            Button(id=1,x=game.width-200, y=game.height-50, width=200, height=50, text="Back to main menu", func=lambda: self.change_menu("main"))
        ]
        super().__init__(game, "game", objects)
        self.camera = Camera(width=game.width, height=game.height)
    def update(self, actions_pressed):
        self.camera.update(actions_pressed)