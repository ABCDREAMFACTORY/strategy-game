from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ..BaseMenu.Menu import Menu
from ...graphics.hud import HUDElement, Button, CityNameLabel, Minimap  
from ...core.Camera import Camera
from ...core.gameManager import GameManager
from ...utils.EventManager import event_manager
from ...core.Enums import Events, ActionType

if TYPE_CHECKING:
    from ...core.City import City
    from ...core.game import Game


class GameMenu(Menu):
    def __init__(self, game: Game):
        self.game: Game = game
        objects: list[Button | Minimap] = [
            Button(id=1,x=game.width-200, y=game.height-50, width=200, height=50, text="Back to main menu", func=lambda: self.back_to_main_menu()),
            Minimap(id=2, x=10, y=game.height-210, width=200, height=200, is_position_relative=False)
        ]
        super().__init__(game, "game", objects)
        self.camera: Camera = Camera(width=game.width, height=game.height)
        self.base_objects: list[HUDElement] = list(objects)

        self.game_manager: GameManager | None = None
        event_manager.subscribe(Events.FOUNDED_CITY, self.on_city_founded)        

    def reset_session(self) -> None:
        self.objects = list(self.base_objects)
        self.current_popup = None
        self.camera.x = 0
        self.camera.y = 0
        self.camera.zoom = 1.0

    def reset(self) -> None:
        self.reset_session()

    def back_to_main_menu(self) -> None:
        self.reset_session()
        self.change_menu("main")

    def update(self, actions_pressed: set[ActionType]) -> None:
        self.camera.update(actions_pressed)

    def on_city_founded(self, city: City) -> None:

        tile_size = self.game.renderer.assets.tile_size
        tile_space = self.game.renderer.assets.tile_space
        co_x, co_y = self.camera.game_to_world(city.pos.x, city.pos.y, tile_size, tile_space) # type: ignore
        co_x += tile_size // 2

        city_name_label = CityNameLabel(id=city.name, x=co_x, y=co_y, city=city)
        self.objects.append(city_name_label)
