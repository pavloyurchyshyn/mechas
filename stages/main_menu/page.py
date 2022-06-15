from visual.UI_base.menu_UI import MenuUI
from visual.UI_buttons.test_draw import TEST_DRAW_BUTTON

from common.global_keyboard import GLOBAL_KEYBOARD

from constants.colors import HALF_EMPTY
from visual.main_window import MAIN_SCREEN
from stages.main_menu.settings.menus_settings.main_menu import MAIN_MENU_BUTTONS, exit_warning, \
    activate_exit_warning_message, deactivate_exit_warning_message, LANG_RELOAD_WARN
from settings.global_parameters import pause_available, pause_step
from constants.game_stages import StagesConstants


class MainMenu(MenuUI):
    def __init__(self):
        super().__init__(buttons=MAIN_MENU_BUTTONS,
                         buttons_objects=[TEST_DRAW_BUTTON, ],
                         name=StagesConstants.MAIN_MENU_STAGE, surface=MAIN_SCREEN)
        self.create_buttons()
        self._fade_surface = self.get_surface(transparent=True)
        self._fade_surface.fill(HALF_EMPTY)
        self._fade_surface.convert_alpha()
        self.add_elements_to_controller(*self._elements, enter_focus=self.start)

    def update(self):
        # VisualEffectsController.update()
        LANG_RELOAD_WARN.update()
        for button in self._elements:
            button.update()

        if GLOBAL_KEYBOARD.ESC and pause_available() and not exit_warning():
            pause_step()
            activate_exit_warning_message()
            self.drop_focused()

        elif GLOBAL_KEYBOARD.ESC and pause_available() and exit_warning():
            pause_step()
            deactivate_exit_warning_message()
            self.drop_focused()

        if self.click():
            xy = self.GLOBAL_MOUSE.pos
            if not exit_warning():
                for button in self._buttons:
                    button.click(xy=xy)
                    if button.clicked:
                        break

            elif not self._exit_yes.click(xy):
                deactivate_exit_warning_message()

    def draw(self, dx=0, dy=0):
        # self._screen.blit(self._surface, (self._x_pic + dx, self._y_pic + dy))
        self._screen.fill((0, 0, 0, 255))
        if self._picture:
            self._screen.blit(self._picture, (self.x0 + dx, self.y0 + dy))
        # VisualEffectsController.draw()

        for element in self._elements:
            element.draw(dx, dy)

        if exit_warning():
            self.surface.blit(self._fade_surface, (0, 0))

            self._exit_no.draw()
            self._exit_yes.draw()

        LANG_RELOAD_WARN.draw()

    def _update(self):
        pass


MAIN_MENU_UI = MainMenu()
