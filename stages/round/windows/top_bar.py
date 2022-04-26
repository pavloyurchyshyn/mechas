from obj_properties.rect_form import Rectangle
from settings.UI_setings.menus_settings.round_menu.top_bar import *
from visual.UI_base.button_UI import Button
from common.global_mouse import GLOBAL_MOUSE
from visual.UIController import UI_TREE
from constants.UI_names import RoundUINames
from datetime import datetime
from visual.font_loader import custom_font_size
from visual.main_window import MAIN_SCREEN


class TopBar(Rectangle):
    name = RoundUINames.TopBar

    def __init__(self, x=X_POS, y=Y_POS, size_x=SIZE_X, size_y=SIZE_Y):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.exit = Button(**EXIT_BUTTON)
        UI_TREE.add_menu(self, self.exit)

        self.time_surface = None
        self.time_pos = (10, 0)
        self.time_font = custom_font_size(20)
        self.current_time = None
        self.update_time()

    def update(self):
        if GLOBAL_MOUSE.delayed_lmb:
            self.exit.click(GLOBAL_MOUSE.pos)

        self.update_time()

    def update_time(self):
        t = datetime.now().strftime('%H:%M')
        if self.current_time != t:
            self.current_time = t
            self.time_surface = self.time_font.render(t, 1, (255, 255, 255))

    def draw(self):
        self.exit.draw()
        MAIN_SCREEN.blit(self.time_surface, self.time_pos)
