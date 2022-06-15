from pygame.constants import K_F4, K_LALT

from common.global_keyboard import GLOBAL_KEYBOARD
from common.stages import Stages
from common.logger import Logger

from constants.game_stages import StagesConstants

from stages.main_menu.page import MAIN_MENU_UI as MAIN_MENU_LOGIC
from stages.round.round_logic import RoundRelatedLogic
from stages.settings.page import SettingsMenu

from visual.UIController import UI_TREE

from common.sound_loader import GLOBAL_MUSIC_PLAYER

LOGGER = Logger().LOGGER


class GameBody:
    def __init__(self):
        self._keyboard = GLOBAL_KEYBOARD
        self.stage_controller = Stages()
        self._stages = {
            StagesConstants.MAIN_MENU_STAGE: self.main_menu,
            StagesConstants.MAIN_MENU_SETTINGS_STAGE: self.setting,

            StagesConstants.CONNECT: self.connect_as_player,
            StagesConstants.HOST: self.host,
            StagesConstants.ROUND_STAGE: self.round,
            StagesConstants.ROUND_CLOSE: self.close_round,
            StagesConstants.EXIT_STAGE: self._close_game,
        }

        self.round_logic: RoundRelatedLogic = RoundRelatedLogic()
        self.settings_in_menu = SettingsMenu()
        self._music_player = GLOBAL_MUSIC_PLAYER
        self._music_player.play_back_music()

    def game_loop(self):
        self._music_player.update()
        self._stages[self.stage_controller.get_current_stage()]()
        UI_TREE.update()
        UI_TREE.draw()
        self._check_alt_and_f4()

    def host(self):
        self.round_logic.host_and_connect()

    def connect_as_player(self):
        self.round_logic.connect_to_server()

    def round(self):
        self.round_logic.round()

    def close_round(self):
        self.round_logic.close_round()

    def host_menu(self):
        pass

    def client_menu(self):
        pass

    def setting(self):
        self.settings_in_menu.update()
        self.settings_in_menu.draw()

    def main_menu(self):
        MAIN_MENU_LOGIC.update()
        MAIN_MENU_LOGIC.draw()

    def _check_alt_and_f4(self):
        # TODO if in round -> save game
        pressed = self._keyboard.pressed
        if pressed[K_F4] and pressed[K_LALT]:
            self._close_game()

    def _close_game(self):
        from pygame import quit as close_program_pygame
        import sys

        close_program_pygame()
        sys.exit()
