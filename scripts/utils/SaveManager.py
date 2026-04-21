import json
import gzip
from pathlib import Path
from typing import Any

from ..map.Map import Map


class SaveManager:
    def __init__(self, game: Any):
        self.game: Any = game
        self.default_save_path: Path = Path("data") / "savegame.json.gz"
    
    def to_dict(self) -> dict[str, Any]:
        return self.game.to_dict()
    
    def save(self, filename: str | Path | None) -> None:
        path = Path(filename) if filename else self.default_save_path
        path.parent.mkdir(parents=True, exist_ok=True)
        data = self.to_dict()
        if path.suffix == ".gz":
            with gzip.open(path, "wt", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        else:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


    def load_game(self, save_path: str | Path | None = None) -> None:
        path = Path(save_path) if save_path else self.default_save_path
        if not path.exists():
            return

        if path.suffix == ".gz":
            with gzip.open(path, "rt", encoding="utf-8") as f:
                data = json.load(f)
        else:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

        self.game.current_turn = data.get("current_turn", 0)
        self.game.players = data.get("players", [])
        map_data = data.get("map")
        if map_data:
            self.game.map = Map.dict_to_map(map_data) # type: ignore
            self.game.width = self.game.map.width
            self.game.height = self.game.map.height
