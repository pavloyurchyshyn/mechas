from pygame.constants import K_F4, K_LALT

from common.global_keyboard import GLOBAL_KEYBOARD
from common.stages import Stages
from common.logger import Logger
from common.sound_loader import GLOBAL_MUSIC_PLAYER

from constants.game_stages import StagesConstants

from stages.main_menu_stage.page import MainMenu
from stages.round_stage.round_logic import RoundRelatedLogic
from stages.settings_stage.page import SettingsMenu
from stages.host_game_stage.page import HostWindow
from stages.join_game_stage.page import JoinWindow
from stages.round_lobby_stage.page import LobbyWindow
from visual.UIController import UI_TREE

LOGGER = Logger()


class GameBody:
    def __init__(self):
        self._keyboard = GLOBAL_KEYBOARD
        self.stage_controller = Stages()
        self._stages = {
            StagesConstants.MAIN_MENU_STAGE: self.main_menu,
            StagesConstants.MAIN_MENU_SETTINGS_STAGE: self.setting,

            StagesConstants.CONNECT: self.connect_as_player,

            StagesConstants.LOAD_HOST: self.load_host_ui,
            StagesConstants.HOST_MENU: self.host_menu_ui,
            StagesConstants.CLOSE_HOST: self.close_host_menu,

            StagesConstants.HOST: self.host,

            StagesConstants.JOIN_MENU: self.join_menu,

            StagesConstants.ROUND_STAGE: self.round,
            StagesConstants.ROUND_CLOSE: self.close_round,
            StagesConstants.EXIT_STAGE: self._close_game,
        }

        self.settings_in_menu = SettingsMenu()
        self._music_player = GLOBAL_MUSIC_PLAYER
        self._music_player.play_back_music()

        self.round_logic: RoundRelatedLogic = RoundRelatedLogic()
        self.main_menu = MainMenu()
        self.host_menu: HostWindow = None
        self.join_menu_ui = JoinWindow()

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
        self.round_logic.update()

    def close_round(self):
        self.round_logic.close_round()

    def load_host_ui(self):
        self.host_menu = HostWindow()
        self.stage_controller.set_host_menu_stage()

    def host_menu_ui(self):
        self.host_menu.update()
        self.host_menu.draw()

    def close_host_menu(self):
        UI_TREE.delete_menu(self.host_menu.name)
        self.host_menu = None
        self.stage_controller.set_main_menu_stage()

    def join_menu(self):
        self.join_menu_ui.update()
        self.join_menu_ui.draw()

    def setting(self):
        self.settings_in_menu.update()
        self.settings_in_menu.draw()

    def main_menu(self):
        self.main_menu.update()
        self.main_menu.draw()

    def _check_alt_and_f4(self):
        # TODO if in round_stage -> save game
        pressed = self._keyboard.pressed
        if pressed[K_F4] and pressed[K_LALT]:
            self._close_game()

    def _close_game(self):
        from pygame import quit as close_program_pygame
        import sys

        close_program_pygame()
        sys.exit()
