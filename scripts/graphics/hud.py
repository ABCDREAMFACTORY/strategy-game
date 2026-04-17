import pygame
from ..core.Enums import ActionType

class HUDElement:
    def __init__(self, id, x, y, is_position_relative=False):
        self.id = id
        self.x = x
        self.y = y
        self.is_position_relative = is_position_relative
    def render(self, screen, font, camera):
        pass
    def update(self, actions_pressed, camera):
        pass
    def on_click(self, mouse_pos, camera):
        pass
    def get_position(self, camera):
        if self.is_position_relative:
            return camera.world_to_screen(self.x, self.y)
        else:
            return self.x, self.y

class Label(HUDElement):
    def __init__(self, id, x, y, text, is_position_relative=False):
        super().__init__(id, x, y, is_position_relative=is_position_relative)
        self.x = x
        self.y = y
        self.text = text

    def render(self, screen, font, camera):
        center = self.get_position(camera)  
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=center)
        screen.blit(text_surf, text_rect)


class Button(HUDElement):
    def __init__(self, id, x, y, width, height, text, func, is_position_relative=False):
        super().__init__(id, x, y, is_position_relative=is_position_relative)
        self.rect = pygame.Rect(x, y, width, height)
        self.label = Label(1,self.rect.centerx, self.rect.centery, text)
        self.func = func

    def render(self, screen, font, camera):
        self.rect.topleft = self.get_position(camera)
        pygame.draw.rect(screen, (100, 100, 100), self.rect)  # Button background
        self.label.render(screen, font, camera)

    def on_click(self, mouse_pos, camera):
        if self.rect.collidepoint(mouse_pos):
            self.func()


class IntSelector(HUDElement):
    def __init__(self, id, x, y, width, height, text, value=0, min_value=None, max_value=None, on_click=None, is_position_relative=False):
        super().__init__(id, x, y, is_position_relative=is_position_relative)
        self.rect = pygame.Rect(x, y, width, height)
        self.label = Label(1,self.rect.centerx, self.rect.centery - 10, text)
        self.value_label = Label(2,self.rect.centerx, self.rect.centery + 10, str(value))
        self.value = value
        self.button_minus = Button(3,x, y, 30, height, "-", self.decrease)
        self.button_plus = Button(4,x + width - 30, y, 30, height, "+", self.increase)
        self.min_value = min_value
        self.max_value = max_value
        self.func = on_click

    def render(self, screen, font, camera):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)  # Background
        self.label.render(screen, font, camera)
        self.value_label.render(screen, font, camera)
        self.button_minus.render(screen, font, camera)
        self.button_plus.render(screen, font, camera)

    def on_click(self, mouse_pos, camera):
        self.button_minus.on_click(mouse_pos, camera)
        self.button_plus.on_click(mouse_pos, camera)

        if self.func is not None:
            self.func()

    def decrease(self):
        if self.value > (self.min_value if self.min_value is not None else float('-inf')):
            self.value -= 1
            self.value_label.text = str(self.value)

    def increase(self):
        if self.value < (self.max_value if self.max_value is not None else float('inf')):
            self.value += 1
            self.value_label.text = str(self.value)


class ListSelector(HUDElement):
    def __init__(self, id, x, y, width, height, text, options: list[str], on_click=None, is_position_relative=False):
        super().__init__(id, x, y, is_position_relative=is_position_relative)
        self.rect = pygame.Rect(x, y, width, height)
        self.label = Label(1,self.rect.centerx, self.rect.centery - 50, text)
        self.options = [Button(i, x, y + i*height, width, height, option, lambda idx=i: self.select(idx)) for i, option in enumerate(options)]
        self.selected_index = None
        self.func = on_click
    def render(self, screen, font, camera):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)  # Background
        for option in self.options:
            option.render(screen, font, camera)
        self.label.render(screen, font, camera)
        

    def on_click(self, mouse_pos, camera):
        selected_index = self.selected_index
        for option in self.options:
            option.on_click(mouse_pos, camera)
        if self.func is not None and selected_index != self.selected_index:
            self.func()

    def select(self, index):
        if not 0 <= index < len(self.options):
            raise ValueError(f"Index {index} is out of range for options list")
        
        self.selected_index = index
        print(f"Selected option: {self.options[index].label.text}")

    def new_list(self, options: list[str]):
        self.options = [Button(i, self.rect.x, self.rect.y + i*self.rect.height, self.rect.width, self.rect.height, option, lambda idx=i: self.select(idx)) for i, option in enumerate(options)]
        self.selected_index = None
    

    def get_value(self):
        if self.selected_index is not None and 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index].label.text
        return None



class CityNameLabel(Label):
    def __init__(self, id, x, y, city):
        super().__init__(id, x, y, city.name, is_position_relative=True)
        self.city = city


class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.camera = None
        self.font = pygame.font.SysFont(None, 24)


    def render(self, current_menu):
        if current_menu.background:
            self.screen.blit(current_menu.background, (0, 0))
        current_menu.render(self.screen, self.font, self.camera)

    def update(self, current_menu, objects: list[HUDElement], actions_pressed, camera):
        self.camera = camera
        for object in objects:
            object.update(actions_pressed, camera) 
        self.on_click(current_menu, actions_pressed, camera)
            
    def on_click(self, current_menu, actions_pressed, camera):
        if ActionType.SELECT in actions_pressed:
            mouse_pos = pygame.mouse.get_pos()
            if current_menu.current_popup is not None:
                current_menu.current_popup.on_click(mouse_pos, camera)
                return
            
            for obj in current_menu.objects:
                obj.on_click(mouse_pos, camera)