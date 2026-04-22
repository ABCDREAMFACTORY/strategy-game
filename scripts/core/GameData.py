

class GameData:
    def __init__(self):
        self.data_civilizations = self.load_civilizations()

    def load_civilizations(self) -> dict[str, dict]:
        import json
        with open("data/config/civilisation.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
        