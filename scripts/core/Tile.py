from .Enums import TerrainType, ResourceType

class Tile:
    def __init__(self, terrain:TerrainType, resource:ResourceType, unit=None, city=None, owner=None, visible=False, explored=False):
        self.terrain = terrain
        self.resource = resource
        self.unit = unit
        self.city = city
        self.owner = owner
        self.visible = visible
        self.explored = explored