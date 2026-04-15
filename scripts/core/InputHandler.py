
import pygame
from .Enums import ActionType

class InputHandler:
    def __init__(self, game):
        self.game = game
        self.actions_pressed = set()
        self.key_bindings = {
            pygame.K_z: ActionType.MOVE_CAMERA_UP,
            pygame.K_s: ActionType.MOVE_CAMERA_DOWN,
            pygame.K_q: ActionType.MOVE_CAMERA_LEFT,
            pygame.K_d: ActionType.MOVE_CAMERA_RIGHT,
            pygame.K_PLUS: ActionType.ZOOMUP,
            pygame.K_MINUS: ActionType.ZOOMDOWN,
            }
        self.event_bindings = {
            pygame.MOUSEBUTTONDOWN: ActionType.SELECT,
            pygame.MOUSEBUTTONUP: ActionType.MOUSEBUTTONUP
            }
        self.is_mouse_down = False


    def handle_event(self, events):
        for key, action in self.event_bindings.items():
            has_found = False
            for event in events:
                if event.type == key and (key != pygame.MOUSEBUTTONDOWN or self.is_mouse_down == False ):
                    self.actions_pressed.add(action)
                    if key == pygame.MOUSEBUTTONDOWN:
                        self.is_mouse_down = True
                    elif key == pygame.MOUSEBUTTONUP:
                        self.is_mouse_down = False
                    has_found = True
                    break
            if has_found == False:
                self.actions_pressed.discard(action)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        for key, action in self.key_bindings.items():
            if keys[key]:
                self.actions_pressed.add(action)
            else:
                self.actions_pressed.discard(action)