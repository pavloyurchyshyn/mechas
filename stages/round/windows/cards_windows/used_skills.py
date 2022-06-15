from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from stages.round.settings.windows_sizes import RoundSizes


class UsedSkillsCards(Rectangle):
    def __init__(self, x=RoundSizes.UsedSkillsCards.X, y=RoundSizes.UsedSkillsCards.Y,
                 size_x=RoundSizes.UsedSkillsCards.X_SIZE, size_y=RoundSizes.UsedSkillsCards.Y_SIZE):
        super(UsedSkillsCards, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

    def update(self):
        pass

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1)
