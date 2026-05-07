from typing import Any, TYPE_CHECKING

class GameData:
    def __init__(self):
        self.data_civilizations:dict[str,dict[str,Any]] = self.load("data/config/civilisation.json")
        self.data_terrains = self.load("data/config/terrains.json")

    @staticmethod
    def load(file:str) -> dict[str, dict[str, Any]]:
        import json
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def load_data(file:str, access:str) -> dict[str, dict[str, Any]]:
        names = access.split("/")
        data = GameData.load(file)
        for name in names:
            data = data[name]
        return data
    
    @staticmethod
    def load_data_(file:str, parent_access:str, child_access:str) -> dict[str, dict[str, Any]]:
        parent_names = parent_access.split("/")
        child_names = child_access.split("/")
        data = GameData.load(file)
        for name in parent_names:
            data = data[name]
        keys = data.keys()
        return {key: GameData.load_data(file, f"{parent_access}/{key}/{child_access}") for key in keys}
game_data = GameData()
        