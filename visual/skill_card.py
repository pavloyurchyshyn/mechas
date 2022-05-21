from pygame.draw import rect as draw_rect
from obj_properties.rect_form import Rectangle
from visual.sprites_functions import get_surface
from visual.main_window import MAIN_SCREEN
from visual.font_loader import DEFAULT_FONT


class SkillCard(Rectangle):
    def __init__(self, x, y, size_x, size_y, text=''):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.text = text
        self.surface = get_surface(size_x=size_x, size_y=size_y, transparent=1)
        self.border_radius = int(size_x * 0.1)

        self.build()

    def build(self):
        self.surface = get_surface(size_x=self.size_x, size_y=self.size_y, transparent=1)
        draw_rect(self.surface, (100, 100, 100), self.surface.get_rect(), border_radius=self.border_radius)
        draw_rect(self.surface, (255, 255, 255), self.surface.get_rect(), 1, border_radius=self.border_radius)
        if self.text:
            c = DEFAULT_FONT.render(str(self.text), 1, (255, 255, 255), 1)
            self.surface.blit(c, (5, 10))

    def update(self):
        pass

    def draw(self):
        MAIN_SCREEN.blit(self.surface, self.left_top)
