import pygame
from pathlib import Path
from ..core.Enums import TerrainType, ResourceType, UnitType, CityType

class AssetsManager:
    def __init__(self, tile_size: int):
        self.tile_size = tile_size
        self.tile_space = 1
        self.missing_tile = pygame.Surface((tile_size, tile_size))
        self.tile_sprites = {}
        self.unit_sprites = {}
        self.city_sprite = self.missing_tile
        self.missing_tile.fill((255, 0, 255))  # debug pink

    def load(self):
        self.tile_sprites = self._load_enum_sprites(TerrainType, Path("assets/tiles"))
        self.unit_sprites = self._load_enum_sprites(UnitType, Path("assets/units"))
        self.city_sprite = self._load(Path("assets/city/city.png"))

    def _load_enum_sprites(self, enum_cls, base_path):
        sprites = {}
        for member in enum_cls:
            path = base_path / f"{member.name.lower()}.png"
            if path.exists():
                sprites[member] = self._load(path)
            else:
                print(f"Warning: Missing sprite for {member} at {path}")
                sprites[member] = self.missing_tile
        return sprites
    
    
    def _load(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (self.tile_size, self.tile_size))
    
    @staticmethod
    def load_image(path, sizex, sizey):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (sizex, sizey))