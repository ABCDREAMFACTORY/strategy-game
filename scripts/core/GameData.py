from typing import Any, TYPE_CHECKING

class GameData:
    def __init__(self):
        self.data_civilizations:dict[str,dict[str,Any]] = self.load("data/config/civilisation.json")
        self.data_terrains = self.load("data/config/terrains.json")

    def load(self, file:str) -> dict[str, dict[str, Any]]:
        import json
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    
game_data = GameData()
        