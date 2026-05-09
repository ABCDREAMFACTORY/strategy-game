import pygame
import random
from .MapGenerator import MapGenerator

class MapVisualisator:
    def __init__(self, map_generator: MapGenerator, screen_width, screen_height, stat):
        self.map_generator = map_generator
        map_generator.gen_matrice()
        self.tiles = map_generator.map_final
        self.tile_size_width = screen_width/len(self.tiles[0])
        self.tile_size_height = screen_height/len(self.tiles)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.stat = stat
        pygame.display.set_caption("Map Visualisator : "+stat)

    def draw_map(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                stat = self.tiles[y][x][self.stat]
                icolor = int(stat*255)
                color = (icolor, icolor, icolor)
                pygame.draw.rect(self.screen, color, (x * self.tile_size_width, y * self.tile_size_height, self.tile_size_width, self.tile_size_height))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_map()
        pygame.quit()

map_visualisator = MapVisualisator(MapGenerator(random.randint(0,9999999), 100, 10), 800, 800, "humidity")
map_visualisator.run()