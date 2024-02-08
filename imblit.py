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

class IMBlit:
    display: pygame.Surface
    size: pygame.Vector2
    should_close: bool = False
    background_color: tuple[int, int, int]
    im_surf: pygame.Surface
    im_pos: pygame.Vector2
    clock: pygame.time.Clock
    gui_msgs: list[tuple[pygame.Surface, pygame.Vector2]]
    font: pygame.font.Font
    gui_last_y: int
    gui_max_width: int
    show_gui: bool

    def __init__(self, resolution: pygame.Vector2, resizable: bool=True, fullscreen: bool=False, background_color: tuple[int, int, int]=(0, 0, 0), title: str="IMBlit window"):
        if fullscreen:
            self.display = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        elif resizable:
            self.display = pygame.display.set_mode(resolution, pygame.RESIZABLE)
        else:
            self.display = pygame.display.set_mode(resolution)
        
        pygame.display.set_caption(title)
        
        self.size = pygame.math.Vector2(resolution)
        self.background_color = background_color
        self.im_surf = None
        self.clock = pygame.time.Clock()
        self.should_close = False
        self._key_press_cb = None
        self._window_resize_cb = None
        self.gui_last_y = 0
        self.gui_max_width = 0
        self.gui_msgs = []
        self.gui_pad = 10
        self.show_gui = True
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets", "font.ttf"), 16)

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

        self.display.fill(self.background_color)
        if self.im_surf != None:
            self.display.blit(self.im_surf, self.im_pos)
        
        if self.show_gui:
            bgrect = pygame.rect.Rect(self.gui_pad/2, self.gui_pad/2, self.gui_max_width+self.gui_pad, self.gui_last_y)
            bgrect.y += 2
            bgrect.x += 2
            pygame.draw.rect(self.display, (80, 20, 20), bgrect, border_radius=4)
            bgrect.y -= 2
            bgrect.x -= 2
            pygame.draw.rect(self.display, (20, 20, 20), bgrect, border_radius=4)
            for surf, pos in self.gui_msgs:
                self.display.blit(surf, pos)
        pygame.display.update()
        self.gui_last_y = 0
        self.gui_msgs = []

        if tick:
            self.clock.tick(tick)
    
    def display_image(self, surface: pygame.Surface, pos: pygame.Vector2=pygame.Vector2(0, 0), center: bool=True, center_x_axis: bool=True, center_y_axis: bool=True, center_scale: bool=True):
        self.im_surf = surface
        self.im_pos = pos
        if center:
            self.center_image(x_axis=center_x_axis, y_axis=center_y_axis, scale=center_scale)
    
    def onkeypress(self, fun):
        self._key_press_cb = fun

    def onwindowresize(self, fun):
        self._window_resize_cb = fun

    def center_image(self, x_axis: bool=True, y_axis: bool=True, scale: bool=True):
        self.size = pygame.Vector2(self.display.get_size())
        width = self.im_surf.get_width()
        height = self.im_surf.get_height()

        if scale:
            width_ratio = width/self.size.x
            height_ratio = height/self.size.y

            ratio = max(width_ratio, height_ratio)

            width = width/ratio
            height = height/ratio

            self.im_surf = pygame.transform.scale(self.im_surf, (width, height))

        self.im_pos = pygame.Vector2()
        if x_axis:
            self.im_pos.x = (self.size.x - width)/2
        if y_axis:
            self.im_pos.y = (self.size.y - height)/2
    
    def add_gui_item(self, message: str):
        pos = pygame.Vector2()
        surf = self.font.render(message, True, (255, 255, 255))
        pos.x = self.gui_pad
        pos.y = self.gui_last_y + self.gui_pad
        self.gui_last_y += surf.get_height() + self.gui_pad
        self.gui_msgs.append((surf, pos))
        if surf.get_width() > self.gui_max_width:
            self.gui_max_width = surf.get_width()