from visual.UI_base.menu_UI import MenuUI
from visual.main_window import MAIN_SCREEN
from constants.game_stages import StagesConstants
from common.stages import Stages
from common.global_keyboard import GLOBAL_KEYBOARD
from common.global_mouse import GLOBAL_MOUSE
from stages.host_game_stage.settings import HOST_BUTTONS_DATA


class HostWindow(MenuUI):
    def __init__(self):
        super(HostWindow, self).__init__(
            buttons=HOST_BUTTONS_DATA,
            name=StagesConstants.HOST_MENU,
            surface=MAIN_SCREEN)

        self.create_buttons()
        self.add_elements_to_controller(*self._elements)

    def update(self):
        if GLOBAL_KEYBOARD.ESC:
            Stages().set_main_menu_stage()

        if GLOBAL_MOUSE.lmb:
            xy = self.GLOBAL_MOUSE.pos
            for button in self._buttons:
                button.click(xy=xy)
                if button.clicked:
                    break

    def draw(self, dx=0, dy=0):
        # self._screen.fill((0, 0, 0, 255))

        for element in self._elements:
            element.draw(dx, dy)
