import json
import pygame
from ..core.gameManager import GameManager
from ..graphics.hud import Button, IntSelector, ListSelector

class Popup:
    def __init__(self, game, name:str, objects = []):
        self.game = game
        self.name = name
        self.is_visible = False
        self.objects = objects  # List of UI elements to display in the popup
        self.overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 200))  # Semi-transparent black
    
    def show(self):
        self.is_visible = True

    def hide(self):
        self.is_visible = False
        self.game.current_menu.current_popup = None

    def render(self, screen, font, camera):
        if self.is_visible:
            screen.blit(self.overlay, (0, 0))
            for obj in self.objects:
                obj.render(screen, font, camera)

    def update(self, actions_pressed):
        if self.is_visible:
            for obj in self.objects:
                obj.update(actions_pressed, camera=self.game.camera)

    def on_click(self, mouse_pos, camera):
        if self.is_visible:
            for obj in self.objects:
                obj.on_click(mouse_pos, camera)

    def getObjectById(self, id) -> object:
        for obj in self.objects:
            if obj.id == id:
                return obj
        return None

class CivilizationSelectorPopup(Popup):
    def __init__(self, game):

        objects = [
            ListSelector(id="civselector", x=500, y=300, width=200, height=50, text="Select Civilization", options=self.get_civilizations(), on_click=self.on_civilization_selected),
            Button(id=1, x=700, y=200, width=100, height=50, text="Close", func=self.hide)
        ]

        super().__init__(game, "civselector", objects=objects)
        
    def on_civilization_selected(self):
        civilization = self.getObjectById("civselector").get_value() # type: ignore
        self.getObjectById("civselector").selected_index = None # type: ignore
        # Handle the logic when a civilization is selected
        print(f"Civilization selected: {civilization}")
        self.hide()

    def get_civilizations(self):
        with open("data/config/civilisation.json", "r") as f:
            civilizations = list(json.load(f).keys())
        return civilizations