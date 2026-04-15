import pygame
from .AssetsManager import AssetsManager


class Renderer:
    def __init__(self, screen: pygame.Surface, camera):
        self.screen = screen
        self.camera = camera

        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.assets = AssetsManager(tile_size=75)
        self.assets.load()
    
    def blit(self, surface:pygame.surface.Surface, x, y):
        screen_x, screen_y = self.camera.game_to_screen(x, y, self.assets.tile_size, self.assets.tile_space)
        self.screen.blit(surface, (screen_x, screen_y))
    
    def render(self, game):
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        if game.current_menu.name == "game":
            self.render_map(game)
        game.hud.render(game.current_menu)
        pygame.display.flip()  # Update the display

    def render_tile(self, tile, x, y):
        sprite = self.assets.tile_sprites.get(tile.terrain, self.assets.missing_tile)
        self.blit(sprite, x, y)

    def render_tiles(self, tiles):
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                self.render_tile(tile, x, y)
            
    def render_border(self, x, y, border_color):
        screen_x, screen_y = self.camera.game_to_screen(x, y, self.assets.tile_size, self.assets.tile_space)
        pygame.draw.rect(self.screen, border_color, (screen_x, screen_y, self.assets.tile_size, self.assets.tile_size), 3)
    
    def render_unit(self, unit, x, y):
        unit_sprite = self.assets.unit_sprites.get(unit.type, self.assets.missing_tile)
        self.blit(unit_sprite, x, y)

    def render_city(self, city, x, y):
        city_sprite = self.assets.city_sprite
        self.blit(city_sprite, x, y)

    def render_map(self, game):
        lowest_visible_x, lowest_visible_y = self.camera.screen_to_game(0, 0, self.assets.tile_size, self.assets.tile_space)
        highest_visible_x, highest_visible_y = self.camera.screen_to_game(self.camera.width, self.camera.height, self.assets.tile_size, self.assets.tile_space)
        for y in range(max(lowest_visible_y, 0), min(highest_visible_y, game.game_manager.map.height - 1) + 1):
            for x in range(max(lowest_visible_x, 0), min(highest_visible_x, game.game_manager.map.width - 1) + 1):
                tile = game.game_manager.map.tiles[y][x]
                self.render_tile(tile, x, y)
                if tile.unit:
                    self.render_unit(tile.unit, x, y)
                if tile.city:
                    self.render_city(tile.city, x, y)
                if tile.owner:
                    self.render_border(x, y, tile.owner.color)