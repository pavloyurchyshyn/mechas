from obj_properties.rect_form import Rectangle
from pygame.draw import rect as draw_rect
from pygame import draw
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes
from visual.main_window import MAIN_SCREEN
from settings.global_parameters import test_draw_status_is_on
from constants.colors import simple_colors

# TODO
class DeckOfCardsWindow(Rectangle):
    def __init__(self,
                 x=RoundSizes.DecksWindow.X, y=RoundSizes.DecksWindow.Y,
                 size_x=RoundSizes.DecksWindow.X_SIZE, size_y=RoundSizes.DecksWindow.Y_SIZE):
        super(DeckOfCardsWindow, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

    def update(self):
        pass

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)

        if test_draw_status_is_on():
            color = simple_colors.yellow
            for dotx, doty in self._dots[1:]:
                draw.circle(MAIN_SCREEN, color, (dotx, doty), 2)
