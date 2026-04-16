
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
        
        BUTTON_LEFT = 1
        BUTTON_RIGHT = 3
        BUTTON_MIDDLE = 2
        SCROLL_UP = 4
        SCROLL_DOWN = 5

        self.mouse_bindings = {
            BUTTON_LEFT: ActionType.SELECT,
        }
        self.is_mouse_down = False


    def handle_events(self, events):
        for key, action in self.event_bindings.items():
            has_found = False
            for event in events:
                has_found = self.handle_event(key, action, event)
            if has_found == False:
                self.actions_pressed.discard(action)
    
    def handle_event(self, key, action, event):
        button = None
        if self.event_is_mouse_button(event):
            if key == pygame.MOUSEBUTTONDOWN and self.is_mouse_down == True:
                return False
            button = event.button
            
        if event.type == key:
            if button is not None:
                if button in self.mouse_bindings:
                    self.actions_pressed.add(action)
                    return True
                else:
                    return False
            self.actions_pressed.add(action)
            if key == pygame.MOUSEBUTTONDOWN:
                self.is_mouse_down = True
            elif key == pygame.MOUSEBUTTONUP:
                self.is_mouse_down = False
            return True
        return False

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        for key, action in self.key_bindings.items():
            if keys[key]:
                self.actions_pressed.add(action)
            else:
                self.actions_pressed.discard(action)

    def event_is_mouse_button(self, event):
        return event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)