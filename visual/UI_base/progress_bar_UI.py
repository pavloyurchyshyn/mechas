from visual.main_window import MAIN_SCREEN, HALF_SCREEN_H, SCREEN_W
from constants.colors import simple_colors, EMPTY
from visual.font_loader import DEFAULT_FONT

from pygame import draw
from pygame import Rect


class ProgressBar:
    MAIN_SCREEN = MAIN_SCREEN

    def __init__(self, screen=None, stage=0, stages_num=1,
                 text=None,
                 bar_pos: (int, int) = None,
                 text_color=simple_colors.white,
                 bar_color=simple_colors.white,
                 border_color=simple_colors.white,
                 bar_x_size: int = None,
                 bar_y_size: int = None,
                 text_pos: (int, int) = None,
                 border_width=1,
                 border_radius=0, out_border_radius=0,
                 border_x_step=1, border_y_step=1):

        self._current_stage = stage
        self.stages_num = stages_num
        self.border_width = border_width

        self.screen = screen if screen else ProgressBar.MAIN_SCREEN
        if self.stages_num != 0:
            self.percent = round(self._current_stage / self.stages_num * 100, 2)
        else:
            self.percent = 0.0
        self._message = text

        self.border_color = border_color
        self.bar_color = bar_color

        self.border_x_step = border_x_step
        self.border_y_step = border_y_step

        self.x_size = bar_x_size - self.border_x_step
        self.y_size = bar_y_size - self.border_y_step
        # =========== text ===================
        self._text = None
        self._text_color = text_color

        if self._message:
            self._render_text()

        self.bar_position = ((SCREEN_W - self.x_size) // 2, HALF_SCREEN_H) if bar_pos is None else bar_pos
        self.bar_position = self.bar_position[0] + self.border_x_step // 2, \
                            self.bar_position[1] + self.border_y_step // 2

        if text_pos:
            self.text_position = text_pos
        else:
            self.text_position = self.bar_position[0], self.bar_position[1] + self.y_size * 2
        # ======================================

        self.border_position = ((SCREEN_W - self.x_size) // 2, HALF_SCREEN_H) if bar_pos is None else bar_pos
        self.border_sizes = (bar_x_size, bar_y_size)
        self.borders_rect = Rect(*self.border_position,
                                 *self.border_sizes)

        self.border_radius = border_radius
        self.out_border_radius = out_border_radius

    def _get_percent(self):
        self.percent = round(self._current_stage / self.stages_num * 100, 2)

    def _render_text(self):
        self._text = DEFAULT_FONT.render(self._message, 1, self._text_color)

    def _bar_endpos(self):
        return self.x_size * (self._current_stage / self.stages_num), self.y_size

    def update(self, current_stage: int = None, text=None, stages_num: int = None, text_pos=None, bar_pos=None,
               bar_color=None):
        if text_pos:
            self.text_position = text_pos

        if bar_color:
            self.bar_color = bar_color

        if bar_pos:
            self.bar_position = bar_pos

        if stages_num is not None:
            self.stages_num = stages_num

        if current_stage is None:
            self._current_stage = int(self._current_stage + 1)
        else:
            self._current_stage = current_stage

        self._get_percent()

        if text:
            self._message = str(text)
            self._render_text()
        else:
            self._text = None

    def change_stages_num(self, num):
        self.stages_num = num

    def change_current_stage(self, num):
        self._current_stage = num

    def draw(self, dx=0, dy=0):
        if self.screen and self.screen != self.MAIN_SCREEN:
            self.screen.fill(EMPTY)

        # BAR
        if self._current_stage:
            draw.rect(surface=self.screen,
                      color=self.bar_color,
                      rect=(self.bar_position, self._bar_endpos()),
                      width=0, border_radius=self.border_radius)

        # BORDER
        if self.border_width:
            draw.rect(surface=self.screen,
                      color=self.border_color,
                      rect=self.borders_rect,
                      width=1, border_radius=self.out_border_radius)

        if self._text:
            self.screen.blit(self._text, self.text_position)

        if self.screen and self.screen != self.MAIN_SCREEN:
            MAIN_SCREEN.blit(self.screen, (0, 0))

    @property
    def values(self):
        return self._current_stage, self.stages_num
