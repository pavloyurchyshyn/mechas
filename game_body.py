from pygame.constants import K_F4, K_LALT

from common.global_keyboard import GLOBAL_KEYBOARD
from common.stages import Stages
from common.logger import Logger

from constants.game_stages import *
from constants.network_keys import NetworkKeys, ServerConnectAnswers

from stages.main_menu.page import MAIN_MENU_UI as MAIN_MENU_LOGIC
from stages.round.page import ROUND_STAGE_LOGIC

from visual.UI_controller import UI_TREE

from network.server.server_controller import ServerController
from network.client.client_network import Network

LOGGER = Logger().LOGGER


class GameBody:
    def __init__(self):
        self._keyboard = GLOBAL_KEYBOARD
        self.stage_controller = Stages()
        self._stages = {
            MAIN_MENU_STAGE: self.main_menu,
            LOADING_STAGE: self.loading_to_round,
            ROUND_STAGE: self.round,
            EXIT_STAGE: self._close_game,
        }

        self.server_controller: ServerController = ServerController()
        self.client: Network = None

    def loading_to_round(self):
        try:
            self.server_controller.run_server()
            self.client = Network()
            response = self.client.connect()
            if self.client.connected:
                LOGGER.info('Client connected')
                self.stage_controller.set_round_stage()
                # from _thread import start_new_thread
                # start_new_thread(self.__round_recv_thread, ())
            else:
                self.client = None
                raise ConnectionError(response.get(NetworkKeys.ServerMessages, ''))

        except Exception as e:
            LOGGER.error(e)
            self.client = None
            self.stage_controller.set_main_menu_stage()

    def host_menu(self):
        pass

    def client_menu(self):
        pass

    def game_loop(self):
        self._stages[self.stage_controller.get_current_stage()]()
        UI_TREE.update()
        UI_TREE.draw()
        self._check_alt_and_f4()

    def __round_recv_thread(self):
        self.stage_controller.set_round_stage()

        while self.client.connected:
            try:
                recv = self.client.receive()
                LOGGER.info(f'Thread {recv}')
            except Exception as e:
                LOGGER.error(e)
                self.stage_controller.set_main_menu_stage()

    def round(self):
        ROUND_STAGE_LOGIC.update()
        ROUND_STAGE_LOGIC.draw()
        self.client.send({'data': 'mmm'})
        # LOGGER.info(self.client.receive())

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
