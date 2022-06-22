from obj_properties.rect_form import Rectangle

from pygame import transform, Surface
from pygame.draw import rect as draw_rect
from pygame.constants import SRCALPHA
from pygame import draw

from visual.UI_base.text_UI import Text
from visual.UIController import UI_TREE
from visual.font_loader import DEFAULT_FONT_SIZE
from visual.main_window import MAIN_SCREEN, SCREEN_W, SCREEN_H

from common.global_clock import GLOBAL_CLOCK

from constants.colors import simple_colors

from settings.screen import Y_SCALE, X_SCALE
from settings.global_parameters import test_draw_status_is_on
from settings.UI_settings.button_settings import ButtonsConst


class Button(Rectangle):
    HELP_TEXT_TIME = 3
    BUTTON_X_SIZE = ButtonsConst.DEFAULT_BUTTON_X_SIZE
    BUTTON_Y_SIZE = ButtonsConst.DEFAULT_BUTTON_Y_SIZE
    CLICK_DELAY = ButtonsConst.DEFAULT_CLICK_DELAY
    CLOCK = GLOBAL_CLOCK
    MAIN_SCREEN = MAIN_SCREEN
    UI_TREE = UI_TREE
    CLICK_ANIMATION_DUR = ButtonsConst.CLICK_ANIMATION_DURATION
    UI_TYPE = 'button'

    def __init__(self, x: int = None, y: int = None,
                 p_x_pos=None, p_y_pos=None,  # percent depends on screen size
                 screen=MAIN_SCREEN,

                 size_x: int = 0, size_y: int = 0,

                 text: str = '',
                 non_active_text=None,
                 text_x=None, text_y=None,
                 change_after_click=0,
                 text_color=simple_colors.white,
                 text_non_active_color=simple_colors.grey,
                 text_size=None,

                 active=True,
                 active_pic=None,

                 on_click_action=None,
                 on_click_action_args: tuple = (),
                 on_click_action_kwargs: dict = {},
                 return_action_value=0,

                 non_active_after_click=0,
                 visible=1,
                 non_visible_after_click=0,

                 picture=None,
                 pic_x=0, pic_y=0,

                 border_color=simple_colors.white,
                 border_width=ButtonsConst.DEFAULT_BORDER_WIDTH,
                 border_non_active_color=simple_colors.grey,
                 border_parameters={},

                 background_color=(0, 0, 0, 120),  # r, g, b, t
                 transparent=0,

                 click_with_delay=True,
                 time_b_click=0.1,
                 id=None,

                 click_anim_dur=None,
                 **kwargs):

        self.id = id
        x = int(x) if x is not None else int(p_x_pos * SCREEN_W)
        if x is None:
            raise Exception(f'{text} X position not defined')

        y = int(y) if y is not None else int(p_y_pos * SCREEN_H)
        if y is None:
            raise Exception(f'{text} Y position not defined')

        size_x = int(size_x * X_SCALE) if size_x else Button.BUTTON_X_SIZE
        size_y = int(size_y * Y_SCALE) if size_y else Button.BUTTON_Y_SIZE
        pic_x = int(pic_x * X_SCALE)
        pic_y = int(pic_y * Y_SCALE)

        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.x = x
        self.y = y

        self.on_click_action = on_click_action
        self.on_click_args = on_click_action_args
        self.on_click_kwargs = on_click_action_kwargs

        self._active = active
        self._visible = visible

        self._change_after_click = change_after_click

        # ---------- TEXT ----------------------
        self._text_text = text
        self._non_active_text_text = non_active_text if non_active_text else text
        self._original_text_size = text_size if text_size else DEFAULT_FONT_SIZE
        self._text_size = self._original_text_size
        self._text_x, self._text_y = int(text_x * X_SCALE) if text_x else text_x, int(
            text_y * Y_SCALE) if text_y else text_y

        self._active_text_color = text_color
        self._inactive_text_color = text_non_active_color

        self._active_text = None
        self._non_active_text = None

        self._active_text_img = None
        self._non_active_text_img = None

        # ---------- BORDER ---------------------
        self._border = None
        self._border_active_color = border_color
        self._border_non_active_color = border_non_active_color
        self._border_width = border_width
        self._border_parameters = border_parameters

        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color

        # ---------- CLICK ----------------------
        self._on_click_action = on_click_action
        self._return_action = return_action_value

        self._non_active_after_click = non_active_after_click
        self._non_visible_after_click = non_visible_after_click

        # ------ PICTURE ------------
        self._picture = picture
        if self._picture:
            self.__scale_picture()
        self._pic_x, self._pic_y = pic_x, pic_y

        # ---------- FINAL PREPARE ---------
        self._screen = screen
        self._button_surface = None  # surface of button for drawing
        self._r_active_button = None
        self._r_non_active_button = None
        self.render()

        if active_pic is None:
            self._current_button_pic = self._r_active_button if active else self._r_non_active_button
        else:
            self._current_button_pic = self._r_active_button if active_pic else self._r_non_active_button

        self._next_click_time = -1
        self._click_with_delay = click_with_delay
        self._time_b_click = time_b_click if time_b_click is not None else Button.CLICK_DELAY

        self._clicked = False
        self._value = None

        self._animation_finish_time = 0
        self._clicked_border = self.get_surface(1, (0, 0, 0, 0))

        draw_rect(self._clicked_border, self._border_active_color, self._clicked_border.get_rect(),
                  int(self._border_width + 2), **self._border_parameters)

        self._click_anim_dur = click_anim_dur if click_anim_dur else self.CLICK_ANIMATION_DUR

    def render(self, scale_k=1):
        self._button_surface = self.get_surface()  # surface of button for drawing

        self._border = self._button_surface.get_rect()

        active_button_s = self.get_surface()  # create background surface
        non_active_button_s = self.get_surface()

        draw_rect(active_button_s, self._background_color, active_button_s.get_rect(), 0, **self._border_parameters)
        draw_rect(non_active_button_s, self._background_color, non_active_button_s.get_rect(), 0,
                  **self._border_parameters)

        self._text_size = self._text_size * scale_k if self._text_size * scale_k >= 1 else self._text_size

        if len(self._text_text) > 0:
            # render text
            self._active_text = Text(text=self._text_text,
                                     screen=active_button_s,
                                     x=self._text_x, y=self._text_y,
                                     color=self._active_text_color,
                                     size=self._text_size)
            self._active_text.draw()  # draw on surface

            self._non_active_text = Text(text=self._text_text,
                                         screen=non_active_button_s,
                                         x=self._text_x, y=self._text_y,
                                         color=self._inactive_text_color,
                                         size=self._text_size)
            self._non_active_text.draw()

        if self._border_width > 0:
            draw_rect(active_button_s, color=self._border_active_color,
                      rect=self._border, width=self._border_width, **self._border_parameters)

            draw_rect(non_active_button_s, color=self._border_non_active_color,
                      rect=self._border, width=self._border_width, **self._border_parameters)

        self._r_active_button = active_button_s  # should be created button picture
        self._r_active_button.convert_alpha()

        self._r_non_active_button = non_active_button_s  # should be created button picture
        self._r_non_active_button.convert_alpha()
        self.define_current_pic()

    def make_original_size(self):
        self._make_original_size()
        self._text_size = self._original_text_size
        self.render()

    def scale(self, k):
        self._scale(k)
        self.render(k)
        if self._picture:
            self.__scale_picture()

    def __scale_picture(self):
        xs, ys = self._picture.get_size()
        if xs > self.size_x or ys > self.size_y:
            if xs > ys:
                k = xs / ys
                self._picture = transform.scale(self._picture, (int(self.size_x), int(self.size_y * k)))
            else:
                k = ys / xs
                self._picture = transform.scale(self._picture, (int(self.size_x * k), int(self.size_y)))

    def set_screen(self, screen):
        self._screen = screen

    def click(self, xy, *args, **kwargs):
        self.UI_TREE.drop_focused()

        if self._active and self.collide_point(xy):
            self._clicked = 1

            if self._click_with_delay:
                time = Button.CLOCK.time
                if self._next_click_time < time:
                    self._next_click_time = time + self._time_b_click
                else:
                    return 0

            self._animation_finish_time = Button.CLOCK.time + self._click_anim_dur

            if self._non_active_after_click:
                self._current_button_pic = self._r_non_active_button
                self._active = 0

            if self._non_visible_after_click:
                self._visible = 0

            if self._on_click_action:
                self._value = self._on_click_action(*self.on_click_args, *args, **self.on_click_kwargs, **kwargs)

            if self._change_after_click:
                self.change_picture()
            else:
                self.define_current_pic()

            return 1

    def define_current_pic(self):
        self._current_button_pic = self._r_active_button if self._active else self._r_non_active_button

    def activate_click(self, *args, **kwargs):
        self.click(self._center, *args, **kwargs)

    def change_picture(self, active=None):
        if active == 1:
            self._current_button_pic = self._r_active_button
        elif active == 0:
            self._current_button_pic = self._r_non_active_button
        else:
            self._current_button_pic = self._r_active_button if self._current_button_pic == self._r_non_active_button else self._r_non_active_button

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)

    def _draw(self, dx=0, dy=0):
        if self._visible:
            if self._picture:
                self._screen.blit(self._picture, (self._pic_x + dx, self._pic_y + dy))

            self._screen.blit(self._current_button_pic, (self.x0 + dx, self.y0 + dy))

            if self.CLOCK.time < self._animation_finish_time:
                self._screen.blit(self._clicked_border, (self.x0 + dx, self.y0 + dy))

            if test_draw_status_is_on():
                color = simple_colors.yellow
                for dotx, doty in self._dots[1:]:
                    draw.circle(Button.MAIN_SCREEN, color, (dotx + dx, doty + dy), 2)

    def update(self):
        self._update()

    def _update(self):
        self._clicked = 0
        self._value = None

    def get_surface(self, transparent=None, back_color=None):
        flags = 0
        transparent = transparent if transparent else self._background_t
        color = back_color if back_color else self._background_color

        if transparent:
            flags = SRCALPHA

        surface = Surface((self.size_x, self.size_y), flags, 32)
        if color:
            surface.fill(color)

        surface.convert_alpha()

        return surface

    def set_active_text(self, text):
        self._text_text = text
        self.render()

    def set_non_active_text(self, text):
        self._non_active_text_text = text
        self.render()

    def set_text_size(self, size):
        self._text_size = size
        self.render()

    def make_visible(self):
        self._visible = 1

    def make_invisible(self):
        self._visible = 0

    def make_active(self):
        self._active = 1
        self.define_current_pic()

    def make_inactive(self):
        self._active = 0
        self.define_current_pic()

    @property
    def text(self):
        return self._text_text

    @text.setter
    def text(self, message):
        self._text_text = message
        self.render()
        # self.define_current_pic()

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = 1 if value else 0

        if self._change_after_click:
            self._current_button_pic = self._r_active_button if self._current_button_pic == self._r_non_active_button else self._r_non_active_button
        else:
            self._current_button_pic = self._r_active_button if self._active else self._r_non_active_button

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def rect(self):
        return self._button_surface.get_rect()

    @property
    def size(self):
        return self.size_x, self.size_y

    @property
    def height(self):
        return self.size_y

    @property
    def width(self):
        return self.size_x

    @property
    def clicked(self):
        return self._clicked

    @property
    def is_active(self):
        return self._active

    @property
    def is_visible(self):
        return self._visible

    def __str__(self):
        return f'Button {self._text_text}'
