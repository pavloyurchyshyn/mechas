from visual.font_loader import DEFAULT_FONT_SIZE
from common.global_clock import GLOBAL_CLOCK
from pygame import Surface
from pygame.transform import rotate, smoothscale
from constants.colors import WHITE
from visual.font_loader import custom_font
from visual.main_window import MAIN_SCREEN, SCREEN_W, SCREEN_H
from visual.UI_base.localization_mixin import LocalizationMixin


class Text(LocalizationMixin):
    CLOCK = GLOBAL_CLOCK
    MIN_Y = 1

    def __init__(self, text, screen=MAIN_SCREEN,
                 raw_text=False,
                 x=None, y=None,
                 color=WHITE,
                 size=None,
                 p_x_pos=None,
                 p_y_pos=None,
                 font_t=None,
                 font_size=None,
                 antial=1,
                 angle=0,
                 auto_draw=True,
                 place_left=False,
                 place_bot=False,
                 place_inside=True,
                 id=None,
                 ):

        self.id = id

        self.raw_text = raw_text

        x = int(x) if x is not None else int(p_x_pos * SCREEN_W) if p_x_pos else None
        y = int(y) if y is not None else int(p_y_pos * SCREEN_H) if p_y_pos else None

        text = str(text)
        self.y0 = y
        self.x0 = x

        self.place_inside = place_inside

        self.font_size = font_size if font_size is not None else DEFAULT_FONT_SIZE
        self._text = text.replace('\t', '    ')
        self._text_font = font_t

        self._r_text_font = None
        self._r_text_img_original = None
        self._r_text_img = None

        self._screen = screen

        self._screen_x_size, self._screen_y_size = self._screen.get_size()

        self._d_time, self._time = Text.CLOCK()

        self._size = size

        self._angle = angle

        self._color = color
        self._antialias = antial

        self.place_left = place_left
        self.place_bot = place_bot
        self.render()

        self.set_x(x)
        self.set_y(y)
        self.auto_draw = auto_draw
        if auto_draw:
            self.draw()

    def set_x(self, x=None):
        if x is None:
            if self.place_left:
                self._x = 1
            else:
                screen_x_size = self._screen.get_width()
                text_x_size = self._r_text_img.get_width()
                text = self.get_text_with_localization(self._text)
                if '\n' in text:
                    l_string = max(text.split('\n'), key=len)
                    l_str_surf = self._r_text_font.render(l_string, self._antialias, self._color)
                    text_x_size = l_str_surf.get_width()

                if text_x_size > screen_x_size:
                    self._x = 1
                else:
                    self._x = screen_x_size // 2 - text_x_size // 2

        else:
            self._x = int(x)

    def set_y(self, y=None):
        if y is None:
            y_s_s = self._screen.get_height()  # s_s -> screen size
            y_t_s = self._r_text_img.get_height()  # t_s -> text size
            text = self.get_text_with_localization(self._text)

            text_size = y_t_s if '\n' not in text else y_t_s * len(text.split('\n'))

            if self.place_bot:
                self._y = y_s_s - text_size
            else:
                if text_size > y_s_s:
                    self._y = 0
                else:
                    self._y = y_s_s // 2 - text_size // 2

        else:
            self._y = int(y)

    def update(self):
        # TODO: for animation and etc. in the future
        pass

    def change_text(self, text):
        self._text = str(text)
        self.render()
        if self.auto_draw:
            self.draw()

    def change_color(self, color):
        if self._color != color:
            self._color = color
            self.render()

    def add_text(self, text):
        self._text = ' '.join((self._text, text))
        self.render()
        if self.auto_draw:
            self.draw()

    def change_pos(self, x, y):
        """
        Change text position

        :return:
        """
        self._x, self._y = int(x), int(y)
        if self.auto_draw:
            self.draw()

    def draw(self, dx=0, dy=0):
        text = self._text if self.raw_text else self.get_text_with_localization(self._text)
        # print(self.id, self.raw_text, self._text, text)

        if '\n' in text:
            # TODO refactor this logic, do render once
            self._size = [0, 0]
            for i, text in enumerate(text.split('\n')):
                t_surf = self._r_text_font.render(text, self._antialias, self._color)
                self._screen.blit(t_surf, (self._x + dx, self._y + dy + self._size[1]))
                self._size[0] = t_surf.get_width() if t_surf.get_width() > self._size[0] else self._size[0]
                self._size[1] += t_surf.get_height()
        else:
            self._screen.blit(self._r_text_img, (self._x + dx, self._y + dy))

    def render(self, raw_text=False):
        self._render_font()
        text = self._text if raw_text or self.raw_text else self.get_text_with_localization(self._text)

        self._r_text_img_original = self._r_text_font.render(text, self._antialias, self._color).convert_alpha()
        x_size = self._r_text_img_original.get_width()
        y_size = self._r_text_img_original.get_height()
        self._r_text_img = self._r_text_img_original.copy()

        if self.place_inside and not self.place_left:
            x_size = self._screen_x_size if self._r_text_img_original.get_width() > self._screen_x_size else self._r_text_img_original.get_width()
            y_size = self._screen_y_size if self._r_text_img_original.get_height() > self._screen_y_size else self._r_text_img_original.get_height()

        if (x_size, y_size) != self._r_text_img_original.get_size():
            self._r_text_img = smoothscale(self._r_text_img_original.copy(), (x_size, y_size))

        if self._angle != 0:
            self._r_text_img = rotate(self._r_text_img, self._angle)

        self._size = self._r_text_img.get_size()

    def _render_font(self):
        try:
            self._r_text_font = custom_font(font_name=self._text_font, size=int(self.font_size))
        except:
            self._r_text_font = custom_font(int(self.font_size))

    @staticmethod
    def get_surface(size_x, size_y):
        surface = Surface((size_x, size_y), 0, 32)

        return surface

    @property
    def size(self):
        return self._size

    @property
    def text(self):
        return self._text

    @property
    def r_text(self):
        return self._r_text_font

    @property
    def sprite(self):
        return self._r_text_img
