from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
# from settings.UI_setings.menus_settings.round_menu.mech_window import *
from settings.UI_setings.menus_settings.round_menu.windows_sizes import RoundSizes


class MechWindow(Rectangle):
    def __init__(self, x=RoundSizes.MechWindow.X, y=RoundSizes.MechWindow.Y,
                 size_x=RoundSizes.MechWindow.X_SIZE, size_y=RoundSizes.MechWindow.Y_SIZE):
        super(MechWindow, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1)