from __future__ import annotations

import pygame
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, cast

from ..core.Enums import ActionType

if TYPE_CHECKING:
    from ..Menus.BaseMenu.Menu import Menu
    from ..core.City import City
    from ..core.Camera import Camera

class HUDElement:
    def __init__(self, id: str | int, x: int | float, y: int | float, is_position_relative: bool = False, layer: int = 0):
        self.id: str | int = id
        self.x: int | float = x
        self.y: int | float = y
        self.is_position_relative: bool = is_position_relative
        self.layer = layer

    def render(self, screen: pygame.Surface, font: pygame.font.Font, camera: Camera) -> None:
        pass

    def update(self, actions_pressed: set[ActionType], camera: Camera) -> None:
        pass

    def on_click(self, mouse_pos: tuple[int, int], camera: Camera) -> None:
        pass

    def get_position(self, camera: Camera) -> tuple[int | float, int | float]:
        if camera is None or not self.is_position_relative:
            return self.x, self.y
        return camera.world_to_screen(self.x, self.y)

class Label(HUDElement):
    def __init__(self, id: str | int, x: int | float, y: int | float, text: str, is_position_relative: bool = False, layer: int = 0):
        super().__init__(id, x, y, is_position_relative=is_position_relative,layer=layer)
        self.x: int | float = x
        self.y: int | float = y
        self.text: str = text

    def render(self, screen: pygame.Surface, font: pygame.font.Font, camera: Camera) -> None:
        center = self.get_position(camera)  
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=center)
        screen.blit(text_surf, text_rect)


class Button(HUDElement):
    def __init__(self, id: str | int, x: int, y: int, width: int, height: int, text: str, func: Callable[[], None], is_position_relative: bool = False, layer: int = 0):
        super().__init__(id, x, y, is_position_relative=is_position_relative, layer=layer)
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.label: Label = Label(1,self.rect.centerx, self.rect.centery, text)
        self.func: Callable[[], None] = func

    def render(self, screen: pygame.Surface, font: pygame.font.Font, camera: Camera) -> None:
        pos_x, pos_y = self.get_position(camera)
        self.rect.topleft = (int(pos_x), int(pos_y))
        pygame.draw.rect(screen, (100, 100, 100), self.rect)  # Button background
        self.label.render(screen, font, camera)

    def on_click(self, mouse_pos: tuple[int, int], camera: Camera) -> None:
        if self.rect.collidepoint(mouse_pos):
            self.func()


class IntSelector(HUDElement):
    def __init__(self, id: str | int, x: int, y: int, width: int, height: int, text: str, value: int = 0, min_value: int | None = None, max_value: int | None = None, on_click: Callable[[], None] | None = None, is_position_relative: bool = False, layer: int = 0):
        super().__init__(id, x, y, is_position_relative=is_position_relative, layer=layer)
        self.rect = pygame.Rect(x, y, width, height)
        self.label = Label(1,self.rect.centerx, self.rect.centery - 10, text)
        self.value_label = Label(2,self.rect.centerx, self.rect.centery + 10, str(value))
        self.value = value
        self.button_minus = Button(3,x, y, 30, height, "-", self.decrease)
        self.button_plus = Button(4,x + width - 30, y, 30, height, "+", self.increase)
        self.min_value = min_value
        self.max_value = max_value
        self.func = on_click

    def render(self, screen: pygame.Surface, font: pygame.font.Font, camera: Camera) -> None:
        pygame.draw.rect(screen, (100, 100, 100), self.rect)  # Background
        self.label.render(screen, font, camera)
        self.value_label.render(screen, font, camera)
        self.button_minus.render(screen, font, camera)
        self.button_plus.render(screen, font, camera)

    def on_click(self, mouse_pos: tuple[int, int], camera: Camera) -> None:
        self.button_minus.on_click(mouse_pos, camera)
        self.button_plus.on_click(mouse_pos, camera)

        if self.func is not None:
            self.func()

    def decrease(self) -> None:
        if self.value > (self.min_value if self.min_value is not None else float('-inf')):
            self.value -= 1
            self.value_label.text = str(self.value)

    def increase(self) -> None:
        if self.value < (self.max_value if self.max_value is not None else float('inf')):
            self.value += 1
            self.value_label.text = str(self.value)


class ListSelector(HUDElement):
    def __init__(self, id: str | int, x: int, y: int, width: int, height: int, text: str, options: list[str], on_click: Callable[[], None] | None = None, is_position_relative: bool = False, layer: int = 0):
        super().__init__(id, x, y, is_position_relative=is_position_relative, layer=layer)
        self.rect = pygame.Rect(x, y, width, height)
        self.label = Label(1,self.rect.centerx, self.rect.centery - 50, text)
        self.options = [Button(i, x, y + i*height, width, height, option, lambda idx=i: self.select(idx)) for i, option in enumerate(options)]
        self.selected_index: int | None = None
        self.func: Callable[[], None] | None = on_click

    def render(self, screen: pygame.Surface, font: pygame.font.Font, camera: Camera) -> None:
        pygame.draw.rect(screen, (100, 100, 100), self.rect)  # Background
        for option in self.options:
            option.render(screen, font, camera)
        self.label.render(screen, font, camera)
        

    def on_click(self, mouse_pos: tuple[int, int], camera: Camera) -> None:
        selected_index = self.selected_index
        for option in self.options:
            option.on_click(mouse_pos, camera)
        if self.func is not None and selected_index != self.selected_index:
            self.func()

    def select(self, index: int) -> None:
        if not 0 <= index < len(self.options):
            raise ValueError(f"Index {index} is out of range for options list")
        
        self.selected_index = index
        print(f"Selected option: {self.options[index].label.text}")

    def new_list(self, options: list[str]) -> None:
        self.options = [Button(i, self.rect.x, self.rect.y + i*self.rect.height, self.rect.width, self.rect.height, option, lambda idx=i: self.select(idx)) for i, option in enumerate(options)]
        self.selected_index = None
    

    def get_value(self) -> str | None:
        if self.selected_index is not None and 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index].label.text
        return None
    
class Minimap(HUDElement):
    def __init__(self, id: str | int, x: int, y: int, width: int, height: int, is_position_relative: bool = False, layer: int = 0):
        super().__init__(id, x, y, is_position_relative=is_position_relative, layer=layer)
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, screen: pygame.Surface, font: pygame.font.Font, camera: Camera) -> None:
        pygame.draw.rect(screen, (50, 50, 50), self.rect)  # Minimap background

class CityNameLabel(Label):
    def __init__(self, id: str | int, x: int | float, y: int | float, city: City, layer: int = 1):
        super().__init__(id, x, y, city.name, is_position_relative=True, layer=layer)
        self.city: City = city


class HUD:
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.camera: Any = None
        self.font: pygame.font.Font = pygame.font.SysFont(None, 24)


    def render(self, current_menu: Menu) -> None:
        if current_menu.background:
            self.screen.blit(current_menu.background, (0, 0))
        current_menu.render(self.screen, self.font, self.camera)

    def update(self, current_menu: Menu, objects: list[HUDElement], actions_pressed: set[ActionType], camera: Camera) -> None:
        self.camera = camera
        for object in objects:
            object.update(actions_pressed, camera) 
        self.on_click(current_menu, actions_pressed, camera)
            
    def on_click(self, current_menu: Menu, actions_pressed: set[ActionType], camera: Camera) -> None:
        if ActionType.SELECT in actions_pressed:
            mouse_pos = pygame.mouse.get_pos()
            if current_menu.current_popup is not None:
                current_menu.current_popup.on_click(mouse_pos, camera)
                return
            
            for obj in current_menu.objects:
                obj.on_click(mouse_pos, camera)