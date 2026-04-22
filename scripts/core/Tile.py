from .Enums import TerrainType, ResourceType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Civ import Civilisation
    from .Player import Player
class Tile:
    def __init__(
        self,
        terrain: TerrainType,
        resource: ResourceType,
        unit: object | None = None,
        city: object | None = None,
        owner: "Player | None" = None,
        visible: bool = False,
        explored: bool = False,
    ) -> None:
        self.terrain: TerrainType = terrain
        self.resource: ResourceType = resource
        self.unit: object | None = unit
        self.city: object | None = city
        self.owner: Player | None = owner
        self.visible: bool = visible
        self.explored: bool = explored