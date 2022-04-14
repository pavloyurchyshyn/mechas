from pygame.constants import K_F4, K_LALT

from common.global_keyboard import GLOBAL_KEYBOARD
from common.stages import Stages

from constants.game_stages import *

from stages.main_menu.page import MAIN_MENU_UI as MAIN_MENU_LOGIC
from stages.round.page import ROUND_STAGE_LOGIC

from visual.UI_controller import UI_TREE


class GameBody:
    def __init__(self):
        self._keyboard = GLOBAL_KEYBOARD
        self._stage_controller = Stages()
        self._stages = {
            MAIN_MENU_STAGE: self.main_menu,
            LOADING_STAGE: self.loading_to_round,
            ROUND_STAGE: self.round,
            EXIT_STAGE: self._close_game,
        }

    def loading_to_round(self):
        self._stage_controller.set_round_stage()

    def game_loop(self):
        self._stages[self._stage_controller.get_current_stage()]()
        UI_TREE.update()
        UI_TREE.draw()
        self._check_alt_and_f4()

    def round(self):
        ROUND_STAGE_LOGIC.update()
        ROUND_STAGE_LOGIC.draw()

    def main_menu(self):
        MAIN_MENU_LOGIC.update()
        MAIN_MENU_LOGIC.draw()

    def _check_alt_and_f4(self):
        # TODO if in round -> save game
        pressed = self._keyboard.pressed
        if pressed[K_F4] and pressed[K_LALT]:
            self._close_game()

    def _close_game(self):
        # self.MULTIPLAYER_CLIENT_DISCONNECT()
        from pygame import quit as close_program_pygame
        import sys

        close_program_pygame()
        sys.exit()
