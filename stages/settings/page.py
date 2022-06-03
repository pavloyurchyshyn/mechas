from visual.UI_base.menu_UI import MenuUI
from settings.UI_setings.menus_settings.main_menu_settings import *
from constants.game_stages import StagesConstants
from common.global_mouse import GLOBAL_MOUSE


class SettingsMenu(MenuUI):
    def __init__(self):
        super(SettingsMenu, self).__init__(buttons=MAIN_MENU_SETTINGS_BUTTONS,
                                           texts=KEYBOARD_TEXT_DATA, texts_objects=KEYBOARD_TEXT_OBJS,
                                           name=StagesConstants.MAIN_MENU_SETTINGS_STAGE,
                                           surface=MAIN_SCREEN)
        self.create_buttons()
        self._music_volume_value = MUSIC_VOLUME_VALUE
        self.add_elements_to_controller(*self._elements, *INPUT_ELEMENTS, MUTE_MUSIC_BUTTON)

    def update(self):
        for inp_el in INPUT_ELEMENTS:
            inp_el.update()

        for button in self._buttons:
            button.update()

        if GLOBAL_KEYBOARD.ESC:  # and pause_available():
            # pause_step()
            Stages().set_main_menu_stage()

        if GLOBAL_MOUSE.lmb:
            xy = self.GLOBAL_MOUSE.pos
            for button in self._buttons:
                button.click(xy=xy)
                if button.clicked:
                    break

            MUTE_MUSIC_BUTTON.click(xy=xy)

    def draw(self, dx=0, dy=0):
        self._screen.fill((0, 0, 0, 255))

        for element in self._elements:
            element.draw(dx, dy)

        self._music_volume_value.draw(dx, dy)

        VOLUME_PROGRESS_BAR.draw(dx, dy)
        MUTE_MUSIC_BUTTON.draw(dx, dy)

        for inp_el in INPUT_ELEMENTS:
            inp_el.draw()

    def _update(self):
        pass
