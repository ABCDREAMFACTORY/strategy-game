from .Enums import ResourceType
from typing import TYPE_CHECKING
from .Position import Position

if TYPE_CHECKING:
    from .Civ import Civilisation
    from .Player import Player
    from .City import City
class Tile:
    def __init__(
        self,
        terrain: str,
        resource: ResourceType,
        unit: object | None = None,
        city: "City | None" = None,
        owner: "Player | None" = None,
        visible: bool = False,
        explored: bool = False,
        pos: Position = Position(0, 0)
    ) -> None:
        self.terrain: str = terrain
        self.resource: ResourceType = resource
        self.unit: object | None = unit
        self.city: City | None = city
        self.owner: Player | None = owner
        self.visible: bool = visible
        self.explored: bool = explored
        self.pos = pos
