from obj_properties.rect_form import Rectangle

from pygame import transform, Surface, mouse
from pygame.draw import rect as draw_rect
from pygame.constants import SRCALPHA
from pygame import draw

from visual.UI_base.text_UI import Text
from common.global_clock import GLOBAL_CLOCK
from common.global_mouse import GLOBAL_MOUSE

from constants.colors import simple_colors
from visual.main_window import MAIN_SCREEN


class ScrollContainer(Rectangle):
    def __init__(self, x, y,
                 screen,
                 size_x, size_y,
                 transparent=1,
                 background_color=(10, 10, 10, 120),  # r, g, b, t
                 border=0, border_color=simple_colors.white,
                 id=None,
                 ):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.id = id

        self._screen = screen
        # --------- BORDER ---------------------
        self._border = border
        self._border_color = border_color

        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color

        self.surface = self.get_surface()

        # -----------------------------------
        self.ui_objects = []
        # -----------------------------------

        self.scroll = 0
        self.elements_height = 0

        self.render()

    def update(self):
        self.check_for_scroll()

        x, y = GLOBAL_MOUSE.x - self.x0, GLOBAL_MOUSE.y - self.y0
        for player_ui_obj in self.ui_objects.copy():
            player_ui_obj.update((x, y))

    def check_for_scroll(self):
        if self.collide_point(GLOBAL_MOUSE.pos):
            if GLOBAL_MOUSE.scroll and self.elements_height > self.size_y:
                self.scroll += GLOBAL_MOUSE.scroll
                if self.scroll > 0:
                    self.scroll = 0

                if self.size_y - self.scroll > self.elements_height:
                    self.scroll = self.size_y - self.elements_height

                self.render()

    def render(self):
        self.calculate_height()
        h = self.scroll + 1

        for el in self.ui_objects:
            el.set_y(h)
            h += el.sizes[1] + 1

    def calculate_height(self):
        self.elements_height = 2
        for el in self.ui_objects:
            self.elements_height += el.size[1] + 1

    def draw(self, dx=0, dy=0):
        pass

    def change_position_lt(self, xy: tuple):
        self._change_position_lt(xy)
        self.render()

    def get_surface(self):
        flags = 0
        if self._background_t:
            flags = SRCALPHA

        surface = Surface((self.size_x, self.size_y), flags, 32)
        if self._background_color:
            surface.fill(self._background_color)

        surface.convert_alpha()

        return surface
