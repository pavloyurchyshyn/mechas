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


class Scroll(Rectangle):
    CLOCK = GLOBAL_CLOCK
    MOUSE = GLOBAL_MOUSE
    STEP_BETWEEN_EL = 5  # pixels

    def __init__(self, x, y,
                 screen,
                 size_x, size_y,
                 transparent=1, background_color=(0, 0, 0, 120),  # r, g, b, t
                 v_step=None,
                 border=0, border_color=simple_colors.white,
                 id=None,
                 ):

        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.id = id

        self._screen = screen
        self._v_step = v_step if v_step else Scroll.STEP_BETWEEN_EL

        # --------- BORDER ---------------------
        self._border = border
        self._border_color = border_color

        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color

        self.surface = self.get_surface()

        # -----------------------------------
        self.elements = []
        # -----------------------------------

        self.scroll = 0
        self.elements_height = 0

        self.render()

    def update(self):
        for button in self.elements:
            button.update()

        if self.collide_point(GLOBAL_MOUSE.pos):
            if GLOBAL_MOUSE.scroll and self.elements_height > self.size_y:
                self.scroll -= GLOBAL_MOUSE.scroll * 2

                if self.scroll > 0:
                    self.scroll = 0

                if self.size_y - self.elements_height > self.scroll:
                    self.scroll = self.size_y - self.elements_height

                self.render()

            if GLOBAL_MOUSE.lmb:
                x, y = GLOBAL_MOUSE.pos
                xy = x-self.x0, y-self.y0
                for button in self.elements:
                    button.click(xy=xy)
                    if button.clicked:
                        break

    def render(self):
        self.calculate_height()
        self.surface.fill(self._background_color)

        h = self.size_y - self.scroll

        for el in reversed(self.elements):
            h -= el.size[1]
            el.set_y(h)
            el.draw()

    def calculate_height(self):
        self.elements_height = 0
        for el in self.elements:
            self.elements_height += el.size[1]

    def draw(self, dx=0, dy=0):
        self._screen.blit(self.surface, (dx + self.x0, dy + self.y0))
        MAIN_SCREEN.blit(self.surface, self.left_top)

        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)

    def change_position_lt(self, xy: tuple):
        self._change_position_lt(xy)
        self.render()

    def add_element(self, element):
        self.elements.append(element)
        self.render()

    def del_element(self, element):
        self.elements.remove(element)
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
