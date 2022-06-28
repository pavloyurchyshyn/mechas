from pygame.draw import rect as draw_rect
from obj_properties.rect_form import Rectangle
from visual.sprites_functions import get_surface
from visual.main_window import MAIN_SCREEN
from visual.font_loader import DEFAULT_FONT, custom_font
from settings.global_parameters import test_draw_status_is_on
from constants.colors import simple_colors
from pygame import draw
from skills.base.skill import BaseSkill
__all__ = ['SkillCard']


class SkillCard(Rectangle):
    def __init__(self, x, y, size_x, size_y, skill: BaseSkill, text=''):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.font = custom_font(size=10)
        self.skill: BaseSkill = skill
        self.text = text if text else skill.name
        self.surface = get_surface(size_x=size_x, size_y=size_y, transparent=1)
        self.border_radius = int(size_x * 0.1)

        self.build()

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