from .Enums import ActionType

class Camera:
    def __init__(self, x=0, y=0, width=1000,height=1000):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zoom = 1.0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_zoom(self, zoom):
        self.zoom = zoom

    def world_to_screen(self, world_x, world_y):
        screen_x = (world_x - self.x) * self.zoom
        screen_y = (world_y - self.y) * self.zoom
        return screen_x, screen_y
    
    def game_to_world(self, game_x, game_y,tile_size, tile_space):
        world_x = game_x*(tile_size+tile_space)
        world_y = game_y*(tile_size+tile_space)
        return world_x, world_y
    
    def game_to_screen(self, game_x, game_y,tile_size, tile_space):
        world_x, world_y = self.game_to_world(game_x, game_y,tile_size, tile_space)
        return self.world_to_screen(world_x, world_y)
    
    def screen_to_world(self, screen_x, screen_y):
        world_x = screen_x / self.zoom + self.x
        world_y = screen_y / self.zoom + self.y
        return world_x, world_y
    
    def world_to_game(self, world_x, world_y,tile_size, tile_space):
        game_x = int(world_x // (tile_size+tile_space))
        game_y = int(world_y // (tile_size+tile_space))
        return game_x, game_y
    
    def screen_to_game(self, screen_x, screen_y,tile_size, tile_space):
        world_x, world_y = self.screen_to_world(screen_x, screen_y)
        return self.world_to_game(world_x, world_y,tile_size, tile_space)
    
    def update(self, actions_pressed):
        if ActionType.MOVE_CAMERA_UP in actions_pressed:
            self.move(0, -10)
        if ActionType.MOVE_CAMERA_DOWN in actions_pressed:
            self.move(0, 10)
        if ActionType.MOVE_CAMERA_LEFT in actions_pressed:
            self.move(-10, 0)
        if ActionType.MOVE_CAMERA_RIGHT in actions_pressed:
            self.move(10, 0)
        # if ActionType.ZOOMUP in actions_pressed:
        #     self.zoom += 1
        # if ActionType.ZOOMDOWN in actions_pressed:
        #     self.zoom -= 0.1