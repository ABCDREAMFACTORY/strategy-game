from ..BaseMenu.Menu import Menu
from ...graphics.hud import Button, CityNameLabel
from ...core.Camera import Camera
from ...utils.EventManager import EventManager, event_manager
from ...core.Enums import Events


class GameMenu(Menu):
    def __init__(self, game):
        self.game = game
        objects = [
            Button(id=1,x=game.width-200, y=game.height-50, width=200, height=50, text="Back to main menu", func=lambda: self.change_menu("main"))
        ]
        super().__init__(game, "game", objects)
        self.camera = Camera(width=game.width, height=game.height)

        self.game_manager = None
        event_manager.subscribe(Events.FOUNDED_CITY, self.on_city_founded)        

    def update(self, actions_pressed):
        self.camera.update(actions_pressed)

    async def on_city_founded(self, city):

        if self.game_manager is None:
            self.game_manager = await event_manager.wait_for(Events.GAME_MANAGER_INITIALIZED)

        tile_size = self.game.renderer.assets.tile_size
        tile_space = self.game.renderer.assets.tile_space
        co_x, co_y = self.camera.game_to_world(city.pos.x, city.pos.y, tile_size, tile_space) # type: ignore
        co_x += tile_size // 2

        city_name_label = CityNameLabel(id=city.name, x=co_x, y=co_y, city=city)
        self.objects.append(city_name_label)
