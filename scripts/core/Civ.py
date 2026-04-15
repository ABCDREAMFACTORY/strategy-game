import json
from .City import City

class Civilisation:
    def __init__(self, game_manager, name, start_position, is_player=True) -> None:
        if game_manager is None:
            raise ValueError("game_manager must be initialized before creating a Civilisation")
        self.game = game_manager
        self.name = name
        data = self.get_data()
        self.color = data["color"]
        self.cities = []
        self.add_city(name=data["cities"][0],pos=start_position)
        self.is_player = is_player
    
    def add_city(self, name, pos):
        for tile_pos in self.game.map.get_tiles_in_radius(self._to_map_coords(pos), radius=1):
            if self.game.map.get_tile(self._to_map_coords(tile_pos)).owner is not None:
                raise ValueError(f"Cannot found city '{name}' at position {pos} because tile at {tile_pos} is already owned by another civilisation")

        self.cities.append(City(name, pos))
        self.game.map.get_tile(self._to_map_coords(pos)).city = self.cities[-1]
        for tile_pos in self.game.map.get_tiles_in_radius(self._to_map_coords(pos), radius=1):
            self.game.map.get_tile(self._to_map_coords(tile_pos)).owner = self

        
        

    def _to_map_coords(self, pos):
        if hasattr(pos, "x") and hasattr(pos, "y"):
            return (pos.x, pos.y)
        return pos
    
    def get_data(self):
        with open("data/config/civilisation.json","r",encoding="utf-8") as f:
            data = json.load(f)[self.name]
        return data