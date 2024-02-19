# Just a simple personal module that just blits images with ui so that i can properly focus on features instead of gui bs
# Not the greatest but works

import os
import sys

# Weaklings have standards
sys.stdout = None
import pygame
pygame.init()
pygame.font.init()
sys.stdout = sys.__stdout__

assets_path = os.path.join(os.path.dirname(__file__), "assets")

# TODO::Share this in all scripts
class Config:
    fullscreen: bool
    resolution: pygame.Vector2 | tuple[int, int]
    resizable: bool
    
    background: tuple[int, int, int]

    scroll_speed: int
    scroll_scale: float

    flash_background: tuple[int, int, int]
    flash_foreground: tuple[int, int, int]

    rgb: bool

    gui_background: tuple[int, int, int]
    gui_foreground: tuple[int, int, int]
    gui_shadow: tuple[int, int, int]


config: Config # MUST BE SET TO CONFIG VALUES BEFORE IMBLIT CONTEXT INIT

def invert_color(color: tuple[int, int, int]):
    r, g, b = color
    return (255 - r, 255 - g, 255 - b)

class IMBlit:
    display: pygame.Surface
    size: pygame.Vector2
    should_close: bool = False
    background_color: tuple[int, int, int]

    image_surface: pygame.Surface
    image_position: pygame.Vector2

    clock: pygame.time.Clock

    font: pygame.font.Font
    font_alert: pygame.font.Font

    gui_element_y: int
    gui_element_width: int
    show_gui: bool
    gui_shadow_offset: int
    gui_shadow_color: list[int, int, int]
    gui_background_color: list[int, int, int]
    gui_background_state: int

    alert_padding: int
    gui_alert_width: int

    messages: list[tuple[pygame.Surface, pygame.Vector2]]
    alerts: list[tuple[pygame.Surface, pygame.Vector2]]

    scroll_speed: int
    scroll_scale: float
    scroll: pygame.Vector2
    scrollable: bool

    resizable: bool
    fullscreen: bool

    framecount: int

    def __init__(self, resolution: pygame.Vector2, resizable: bool=True, fullscreen: bool=False, background_color: tuple[int, int, int]=(0, 0, 0), title: str="IMBlit window"):
        if fullscreen:
            self.display = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        elif resizable:
            self.display = pygame.display.set_mode(resolution, pygame.RESIZABLE)
        else:
            self.display = pygame.display.set_mode(resolution)

        self.font = pygame.font.Font(os.path.join(assets_path, "font.ttf"), 16)
        self.font = pygame.font.Font(os.path.join(assets_path, "font.ttf"), 18)
        icon = pygame.image.load(os.path.join(assets_path, "icon.png"))
        pygame.display.set_caption(title)
        pygame.display.set_icon(icon)
        
        self.size = pygame.math.Vector2(resolution)
        self.background_color = config.background or background_color
        self.image_surface = None
        
        self._key_press_cb = None
        self._window_resize_cb = None
        self._mouse_button_down_cb = None
        self._mouse_button_up_cb = None

        self.clock = pygame.time.Clock()
        self.should_close = False
        self.messages = []

        self.show_gui = True
        self.gui_element_y = 0
        self.gui_element_width = 0
        self.gui_padding = 10
        self.gui_shadow_offset = 3
        self.gui_shadow_color = config.gui_shadow or [20, 40, 80]
        self.gui_background_color = config.gui_background or [20, 20, 20]
        self.gui_background_state = 0

        self.gui_alert_width = 0
        self.alert_padding = 20
        self.alerts = []

        self.resizable = resizable
        self.fullscreen = fullscreen

        self.framecount = 0
        self.scrollable = True
        self.scroll_speed = 4
        self.scroll_scale = 1.5
        self.scroll = pygame.Vector2(0, 0)

    def update(self, tick: int | None=None):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.should_close = True
            elif e.type == pygame.KEYDOWN:
                if self._key_press_cb:
                    self._key_press_cb(e.key)
            elif e.type == pygame.WINDOWRESIZED:
                if self._window_resize_cb:
                    self._window_resize_cb()
            elif e.type == pygame.MOUSEWHEEL:
                self.scroll.y += self.scroll_speed * e.y * 4
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if self._mouse_button_down_cb:
                    self._mouse_button_down_cb(e.button)
            elif e.type == pygame.MOUSEBUTTONUP:
                if self._mouse_button_up_cb:
                    self._mouse_button_up_cb(e.button)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.scroll.y -= self.scroll_speed
        elif keys[pygame.K_UP]:
            self.scroll.y += self.scroll_speed

        self.display.fill(self.background_color)
        if self.image_surface != None:
            if self.scrollable:
                if self.scroll.y > 0:
                    self.scroll.y = 0
                # HACK: FIXME: TODO
                imgbottom = self.scroll.y + self.image_surface.get_height()
                if imgbottom < self.display.get_height():
                    self.scroll.y = -(self.image_surface.get_height() - self.display.get_height())
                self.display.blit(self.image_surface, self.image_position+self.scroll)
            else:
                self.display.blit(self.image_surface, self.image_position)
        if self.show_gui:
            if config.rgb:
                self.apply_gui_special_effects()
            background_rect = pygame.rect.Rect((self.gui_padding/2) + self.gui_shadow_offset, (self.gui_padding/2) + self.gui_shadow_offset, self.gui_element_width+self.gui_padding, self.gui_element_y)
            pygame.draw.rect(self.display, self.gui_shadow_color, background_rect, border_radius=4)
            background_rect.x -= self.gui_shadow_offset
            background_rect.y -= self.gui_shadow_offset
            pygame.draw.rect(self.display, self.gui_background_color, background_rect, border_radius=4)
            for surface, position in self.messages:
                self.display.blit(surface, position)
            
            position = pygame.Vector2(self.size.x - self.gui_alert_width - self.gui_padding)
            position.y = self.gui_padding

            for alert in self.alerts:
                if config.flash_foreground:
                    color = config.flash_foreground
                elif config.rgb:
                    color = invert_color(self.gui_shadow_color)
                else:
                    color = (255, 255, 255)

                surf = self.font.render(alert, True, color)

                background_rect = pygame.rect.Rect(position.x - self.gui_padding/2, position.y - self.gui_padding/2, surf.get_width() + self.gui_padding, surf.get_height() + self.gui_padding)
                if config.flash_background:
                    bg_color = config.flash_background
                elif config.rgb:
                    bg_color = self.gui_shadow_color
                else:
                    bg_color = (25, 25, 25)

                pygame.draw.rect(self.display, bg_color, background_rect, border_radius=4)
                
                self.display.blit(surf, position)
                position.y += surf.get_height() + self.alert_padding

        pygame.display.update()
        self.gui_alert_width = 0
        self.gui_alert_y = 0
        self.alerts = []

        self.gui_element_width = 0
        self.gui_element_y = 0
        self.messages = []
    

        if tick:
            self.clock.tick(tick)
        
        self.framecount += 1
    
    def display_image(self, surface: pygame.Surface, pos: pygame.Vector2=pygame.Vector2(0, 0), center: bool=True, center_x_axis: bool=True, center_y_axis: bool=True, center_scale: bool=True):
        self.image_surface = surface
        self.image_position = pos
        if center:
            self.center_image(x_axis=center_x_axis, y_axis=center_y_axis, scale=center_scale)
    
    def onkeypress(self, fun):
        self._key_press_cb = fun

    def onwindowresize(self, fun):
        self._window_resize_cb = fun

    def onmousebuttondown(self, fun):
        self._mouse_button_down_cb = fun
    
    def onmousebuttonup(self, fun):
        self._mouse_button_up_cb = fun

    def center_image(self, x_axis: bool=True, y_axis: bool=True, scale: bool=True):
        self.size = pygame.Vector2(self.display.get_size())
        width = self.image_surface.get_width()
        height = self.image_surface.get_height()
        self.scroll = pygame.Vector2(0, 0)

        if scale:
            width_ratio = width/self.size.x
            height_ratio = height/self.size.y

            ratio = max(width_ratio, height_ratio)

            width = width/ratio
            height = height/ratio

            if self.scrollable:
                width *= self.scroll_scale
                height *= self.scroll_scale

            self.image_surface = pygame.transform.scale(self.image_surface, (width, height))

        self.image_position = pygame.Vector2()
        if x_axis:
            self.image_position.x = (self.size.x - width)/2
        if y_axis and not self.scrollable:
            self.image_position.y = (self.size.y - height)/2
    
    def add_gui_item(self, message: str):   
        if config.gui_foreground:
            color = config.gui_foreground
        else:
            color = (255, 255, 255)
        pos = pygame.Vector2()
        surf = self.font.render(message, True, color)
        pos.x = self.gui_padding
        pos.y = self.gui_element_y + self.gui_padding
        self.gui_element_y += surf.get_height() + self.gui_padding
        self.messages.append((surf, pos))
        if surf.get_width() > self.gui_element_width:
            self.gui_element_width = surf.get_width()
    
    def toggle_fullscreen(self, resolution: pygame.Vector2 = None):
        if resolution:
            resolution = pygame.Vector2(resolution)
        else:
            resolution = self.size

        if not self.fullscreen:
            self.display = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
            self.fullscreen = True
        elif self.resizable:
            self.display = pygame.display.set_mode(resolution, pygame.RESIZABLE)
            self.fullscreen = False
        else:
            self.display = pygame.display.set_mode(resolution)
            self.fullscreen = False
    
    def apply_gui_special_effects(self):
        if config.rgb:
            gui_shadow_color_change_rate = 3
            if self.gui_background_state == 0:
                self.gui_shadow_color[0] += gui_shadow_color_change_rate
                if self.gui_shadow_color[0] >= 255:
                    self.gui_background_state = 1
                    self.gui_shadow_color[0] = 255
            elif self.gui_background_state == 1:
                self.gui_shadow_color[1] += gui_shadow_color_change_rate
                if self.gui_shadow_color[1] >= 255:
                    self.gui_background_state = 2
                    self.gui_shadow_color[1] = 255
            elif self.gui_background_state == 2:
                self.gui_shadow_color[2] += gui_shadow_color_change_rate
                if self.gui_shadow_color[2] >= 255:
                    self.gui_background_state = 3
                    self.gui_shadow_color[2] = 255
            elif self.gui_background_state == 3:
                self.gui_shadow_color[0] -= gui_shadow_color_change_rate
                if self.gui_shadow_color[0] <= 0:
                    self.gui_background_state = 4
                    self.gui_shadow_color[0] = 0
            elif self.gui_background_state == 4:
                self.gui_shadow_color[1] -= gui_shadow_color_change_rate
                if self.gui_shadow_color[1] <= 0:
                    self.gui_background_state = 5
                    self.gui_shadow_color[1] = 0
            elif self.gui_background_state == 5:
                self.gui_shadow_color[2] -= gui_shadow_color_change_rate
                if self.gui_shadow_color[2] <= 0:
                    self.gui_background_state = 0
                    self.gui_shadow_color[2] = 0
        else:
            self.gui_shadow_color = config.gui_shadow
    
    def add_alert(self, message: str):
        demo = self.font.render(message, True, (255, 255, 255))
        self.alerts.append(message)
        if demo.get_width() > self.gui_alert_width:
            self.gui_alert_width = demo.get_width()
        