from obj_properties.rect_form import Rectangle

from pygame.draw import rect as draw_rect
from pygame import draw

from settings.global_parameters import test_draw_status_is_on

from constants.colors import simple_colors

from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes

from visual.main_window import MAIN_SCREEN
from settings.screen import GAME_SCALE
from visual.sprites_functions import get_surface
from visual.font_loader import DEFAULT_FONT, custom_font
from visual.UI_base.text_UI import Text


class BaseCard(Rectangle):
    def __init__(self, unique_id,
                 x=RoundSizes.CardSize.X,
                 y=RoundSizes.CardSize.Y,
                 size_x=RoundSizes.CardSize.X_SIZE,
                 size_y=RoundSizes.CardSize.Y_SIZE,
                 title_text=''):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.unique_id = unique_id
        self.font = DEFAULT_FONT
        self.title_text: str = title_text

        self.surface = None
        self.title_text_obj: Text = None
        self.border_radius = int(size_x * 0.1)

        self.chosen = False
        self.build()

    def build(self):
        self.surface = get_surface(size_x=self.size_x, size_y=self.size_y, transparent=1)

        draw_rect(self.surface, simple_colors.grey3, self.surface.get_rect(), border_radius=self.border_radius)
        draw_rect(self.surface, simple_colors.white, self.surface.get_rect(), 1, border_radius=self.border_radius)

        self.title_text_obj = Text(self.title_text,
                                   screen=self.surface,
                                   font_size=11*GAME_SCALE,
                                   x=self.size_x * .1, y=self.size_y * .01,
                                   size=(self.size_x * 0.8, self.size_y * .02)
                                   )

    def chose(self):
        self.chosen = True

    def unchoose(self):
        self.chosen = False

    def draw(self):
        MAIN_SCREEN.blit(self.surface, self.left_top)
        if test_draw_status_is_on():
            color = simple_colors.yellow
            for dotx, doty in self._dots[1:]:
                draw.circle(MAIN_SCREEN, color, (dotx, doty), 2)
