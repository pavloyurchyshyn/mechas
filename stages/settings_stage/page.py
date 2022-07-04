from visual.UI_base.menu_UI import MenuUI
from stages.settings_stage.settings import *
from stages.settings_stage.settings.nickname import NICKNAME_input

from constants.game_stages import StagesConstants
from common.global_mouse import GLOBAL_MOUSE
from common.stages import Stages
from common.global_keyboard import GLOBAL_KEYBOARD
from visual.main_window import MAIN_SCREEN


class SettingsMenu(MenuUI):
    def __init__(self):
        super(SettingsMenu, self).__init__(buttons=MAIN_MENU_SETTINGS_BUTTONS_DATA,
                                           texts=MAIN_MENU_SETTINGS_TEXTS_DATA,
                                           name=StagesConstants.MAIN_MENU_SETTINGS_STAGE,
                                           surface=MAIN_SCREEN)
        self.add_elements_to_controller(NICKNAME_input)
        self.create_buttons()
        self.create_text()
        # self._music_volume_value = MUSIC_VOLUME_VALUE
        self.add_elements_to_controller(*self._elements)  # , *INPUT_ELEMENTS, MUTE_MUSIC_BUTTON)

    def update(self):
        # for inp_el in INPUT_ELEMENTS:
        #     inp_el.update()

        for button in self._buttons:
            button.update()

        if GLOBAL_KEYBOARD.ESC:
            Stages().set_main_menu_stage()

        if GLOBAL_MOUSE.lmb:
            xy = self.GLOBAL_MOUSE.pos
            for button in self._buttons:
                button.click(xy=xy)
                if button.clicked:
                    break

            # MUTE_MUSIC_BUTTON.click(xy=xy)

        NICKNAME_input.update()

    def draw(self, dx=0, dy=0):
        self._screen.fill((0, 0, 0, 255))

        for element in self._elements:
            element.draw(dx, dy)

        # self._music_volume_value.draw(dx, dy)

        VOLUME_PROGRESS_BAR.draw(dx, dy)
        NICKNAME_input.draw()
        # MUTE_MUSIC_BUTTON.draw(dx, dy)

        # for inp_el in INPUT_ELEMENTS:
        #     inp_el.draw()

    def _update(self):
        pass
