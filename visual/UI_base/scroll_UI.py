from obj_properties.rect_form import Rectangle

from pygame import transform, Surface, mouse
from pygame.draw import rect as DrawRect
from pygame.constants import SRCALPHA
from pygame import draw

from visual.UI_base.text_UI import Text
from common.global_clock import GLOBAL_CLOCK
from common.global_mouse import GLOBAL_MOUSE

from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE, \
    DEFAULT_BUTTON_Y_SIZE, DEFAULT_CLICK_DELAY
from constants.colors import simple_colors


class Scroll(Rectangle):
    BUTTON_X_SIZE = DEFAULT_BUTTON_X_SIZE
    BUTTON_Y_SIZE = DEFAULT_BUTTON_Y_SIZE
    CLICK_DELAY = DEFAULT_CLICK_DELAY
    CLOCK = GLOBAL_CLOCK
    MOUSE = GLOBAL_MOUSE
    STEP_BETWEEN_EL = 5  # pixels

    def __init__(self, x, y,
                 screen,
                 size_x=None, size_y=None,
                 transparent=0, background_color=(0, 0, 0, 120),  # r, g, b, t
                 ui_elements=[],
                 h_step=None, v_step=None,
                 border=0, border_color=simple_colors.white,
                 id=None,
                 ):
        size_x = size_x if size_x else Scroll.BUTTON_X_SIZE
        size_y = size_y if size_y else Scroll.BUTTON_Y_SIZE

        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.id = id

        self._screen = screen
        self._h_step = h_step if h_step else Scroll.STEP_BETWEEN_EL
        self._v_step = v_step if v_step else Scroll.STEP_BETWEEN_EL

        # --------- BORDER ---------------------
        self._border = border
        self._border_color = border_color

        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color

        self._main_surface = self.get_surface()
        self._surface = None

        # -----------------------------------
        self._ui_elements = ui_elements
        self._elements_data = []
        # -----------------------------------

        self._draw_dx_dy = [0, 0]

        self.build()

    def build(self):
        self._elements_data.clear()

        self._surface = self.get_surface()



    def update(self):
        ts, bs = Scroll.MOUSE.scroll

    def click(self, xy):

        xy = Scroll.MOUSE.pos

    def draw(self, dx=0, dy=0):
        self._screen.blit(self._main_surface, (dx + self.x0, dy + self.y0))
        for element in self._elements_data:
            element.draw(dx+self.x0, dy + self.y0)

    def change_position_lt(self, xy: tuple):
        self._change_position_lt(xy)
        self.build()

    def add_element(self, element):
        self._elements_data.append(element)

    def del_element(self):
        pass

    def get_surface(self):
        flags = 0
        if self._background_t:
            flags = SRCALPHA

        surface = Surface((self.size_x, self.size_y), flags, 32)
        if self._background_color:
            surface.fill(self._background_color)

        surface.convert_alpha()

        return surface
