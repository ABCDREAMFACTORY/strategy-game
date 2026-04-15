from .Civ import Civilisation

class Player:
    def __init__(self, game, civ_name, start_position) -> None:
        self.game = game
        self.civ_name = civ_name
        self.start_position = start_position
        self.civ = None

    def initialize_civilisation(self, game_manager):
        self.civ = Civilisation(game_manager, self.civ_name, self.start_position)