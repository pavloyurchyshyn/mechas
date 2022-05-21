from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from settings.UI_setings.menus_settings.round_menu.windows_sizes import RoundSizes


class ChatWindow(Rectangle):
    def __init__(self, x=RoundSizes.ChatWindow.X, y=RoundSizes.ChatWindow.Y,
                 size_x=RoundSizes.ChatWindow.X_SIZE, size_y=RoundSizes.ChatWindow.Y_SIZE):
        super(ChatWindow, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1)