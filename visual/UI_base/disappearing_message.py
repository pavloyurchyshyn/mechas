from obj_properties.rect_form import Rectangle
from visual.UI_base.text_UI import Text
from visual.sprites_functions import get_surface
from time import time
from visual.main_window import MAIN_SCREEN


class DisappMessage(Rectangle):
    def __init__(self, text, x, y, size_x, size_y=None, exists_time=1, screen=MAIN_SCREEN, id=None):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.id = id

        self.screen = screen

        self.exists_time = exists_time
        self.disappearing_time = 0

        self.text_value = text
        print('TEXT', text)
        self.surface = get_surface(self.size_x, self.size_y, 1, color=(0, 0, 0, 200))
        self.text = Text(text, self.surface, x=0, y=0)
        self._visible = True

    def update_surface(self):
        self.surface.fill((0, 0, 0, 200))
        self.text.draw()

    def activate(self):
        self._visible = True
        self.disappearing_time = time() + self.exists_time

    def update(self):
        if self._visible:
            if self.disappearing_time < time():
                self._visible = False

    def draw(self):
        if self._visible:
            self.screen.blit(self.surface, self.left_top)
