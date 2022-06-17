from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from stages.round.settings.windows_sizes import RoundSizes


class DiceWindow(Rectangle):
    def __init__(self):
        super(DiceWindow, self).__init__(x=RoundSizes.Dice.X, y=RoundSizes.Dice.Y,
                                         size_x=RoundSizes.Dice.X_SIZE,
                                         size_y=RoundSizes.Dice.Y_SIZE)

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
