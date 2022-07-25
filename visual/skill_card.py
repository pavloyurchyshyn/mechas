from pygame.draw import rect as draw_rect
from obj_properties.rect_form import Rectangle
from visual.sprites_functions import get_surface
from visual.main_window import MAIN_SCREEN
from visual.font_loader import DEFAULT_FONT, custom_font
from settings.global_parameters import test_draw_status_is_on
from constants.colors import simple_colors
from pygame import draw
from skills.base.skill import BaseSkill
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes

__all__ = ['SkillCard', ]


class SkillCard(Rectangle):
    def __init__(self, skill: BaseSkill,
                 x=RoundSizes.CardSize.X,
                 y=RoundSizes.CardSize.Y,
                 size_x=RoundSizes.CardSize.X_SIZE,
                 size_y=RoundSizes.CardSize.Y_SIZE,
                 text=''):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.font = custom_font(size=10)
        self.skill: BaseSkill = skill
        self.unique_id = self.skill.unique_id
        self.text = text if text else skill.name
        self.surface = get_surface(size_x=size_x, size_y=size_y, transparent=1)
        self.border_radius = int(size_x * 0.1)

        self.chosen = False

        self.build()

    def chose(self):
        self.chosen = True

    def unchoose(self):
        self.chosen = False

    def build(self):
        self.surface = get_surface(size_x=self.size_x, size_y=self.size_y, transparent=1)
        draw_rect(self.surface, (100, 100, 100), self.surface.get_rect(), border_radius=self.border_radius)
        draw_rect(self.surface, (255, 255, 255), self.surface.get_rect(), 1, border_radius=self.border_radius)
        if self.text:
            c = self.font.render(str(self.text), 1, (255, 255, 255), 1)
            self.surface.blit(c, (5, 10))

    def update(self):
        pass

    def draw(self):
        MAIN_SCREEN.blit(self.surface, self.left_top)
        if test_draw_status_is_on():
            color = simple_colors.yellow
            for dotx, doty in self._dots[1:]:
                draw.circle(MAIN_SCREEN, color, (dotx, doty), 2)
