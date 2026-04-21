from __future__ import annotations

import pygame
from typing import TYPE_CHECKING, Any, cast

from .AssetsManager import AssetsManager

if TYPE_CHECKING:
    from ..core.Camera import Camera
    from ..core.Tile import Tile
    from ..core.game import Game
    from ..Menus.GameScreen.Game import GameMenu


class Renderer:
    def __init__(self, screen: pygame.Surface, camera: Camera):
        self.screen: pygame.Surface = screen
        self.camera: Camera = camera

        self.font: pygame.font.Font = pygame.font.Font(None, 24)
        self.small_font: pygame.font.Font = pygame.font.Font(None, 18)
        self.assets: AssetsManager = AssetsManager(tile_size=75)
        self.assets.load()
    
    def blit(self, surface: pygame.Surface, x: int, y: int) -> None:
        screen_x, screen_y = self.camera.game_to_screen(x, y, self.assets.tile_size, self.assets.tile_space)
        self.screen.blit(surface, (screen_x, screen_y))
    
    def render(self, game: Game) -> None:
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        if game.current_menu.name == "game":
            self.render_map(game)
        game.hud.render(game.current_menu)
        pygame.display.flip()  # Update the display

    def render_tile(self, tile: Tile, x: int, y: int) -> None:
        sprite = self.assets.tile_sprites.get(tile.terrain, self.assets.missing_tile)
        self.blit(sprite, x, y)

    def render_tiles(self, tiles: list[list[Tile]]) -> None:
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                self.render_tile(tile, x, y)
            
    def render_border(self, x: int, y: int, border_color: tuple[int, int, int]) -> None:
        screen_x, screen_y = self.camera.game_to_screen(x, y, self.assets.tile_size, self.assets.tile_space)
        pygame.draw.rect(self.screen, border_color, (screen_x, screen_y, self.assets.tile_size, self.assets.tile_size), 3)
    
    def render_unit(self, unit: Any, x: int, y: int) -> None:
        unit_sprite = self.assets.unit_sprites.get(unit.type, self.assets.missing_tile)
        self.blit(unit_sprite, x, y)

    def render_city(self, city: object, x: int, y: int) -> None:
        city_sprite = self.assets.city_sprite
        self.blit(city_sprite, x, y)

    def render_map(self, game: Game) -> None:
        game_menu:GameMenu = game.menus["game"] # type: ignore
        game_manager = game_menu.game_manager
        if game_manager is None:
            return

        lowest_visible_x, lowest_visible_y = self.camera.screen_to_game(0, 0, self.assets.tile_size, self.assets.tile_space)
        highest_visible_x, highest_visible_y = self.camera.screen_to_game(self.camera.width, self.camera.height, self.assets.tile_size, self.assets.tile_space)
        for y in range(max(lowest_visible_y, 0), min(highest_visible_y, game_manager.map.height - 1) + 1):
            for x in range(max(lowest_visible_x, 0), min(highest_visible_x, game_manager.map.width - 1) + 1):
                tile = game_manager.map.tiles[y][x]
                self.render_tile(tile, x, y)
                if tile.unit:
                    self.render_unit(tile.unit, x, y)
                if tile.city:
                    self.render_city(tile.city, x, y)
                if tile.owner:
                    owner = cast(Any, tile.owner)
                    self.render_border(x, y, owner.color)