from enum import Enum

class ResourceType(Enum):
    NONE = -1
    FOOD = 0
    WOOD = 1
    STONE = 2
    GOLD = 3    

class UnitType(Enum):
    WORKER = 0
    SOLDIER = 1
    ARCHER = 2
    KNIGHT = 3

class CityType(Enum):
    VILLAGE = 0
    TOWN = 1
    CITY = 2

class ActionType(Enum):
    MOVE_CAMERA_UP = 0
    MOVE_CAMERA_DOWN = 1
    MOVE_CAMERA_LEFT = 2
    MOVE_CAMERA_RIGHT = 3
    SELECT = 4
    MOUSEBUTTONUP = 5
    ZOOMUP = 6
    ZOOMDOWN = 7

class GameState(Enum):
    MAIN_MENU = 0
    IN_GAME = 1
    PAUSED = 2
    GAME_OVER = 3

class Events(Enum):
    TILE_CLICKED = 0
    FOUNDED_CITY = 1
    GAME_MANAGER_INITIALIZED = 2