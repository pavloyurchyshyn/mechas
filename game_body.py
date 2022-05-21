from pygame.constants import K_F4, K_LALT

from _thread import start_new_thread

from common.global_keyboard import GLOBAL_KEYBOARD
from common.stages import Stages
from common.logger import Logger

from constants.game_stages import StagesConstants
from constants.network_keys import NetworkKeys

from stages.main_menu.page import MAIN_MENU_UI as MAIN_MENU_LOGIC
from stages.round.page import ROUND_STAGE_LOGIC

from visual.UIController import UI_TREE

from network.server.server_controller import ServerController
from network.client.client_network import Network

LOGGER = Logger().LOGGER


class GameBody:
    def __init__(self):
        self._keyboard = GLOBAL_KEYBOARD
        self.stage_controller = Stages()
        self._stages = {
            StagesConstants.MAIN_MENU_STAGE: self.main_menu,
            StagesConstants.LOADING_STAGE: self.loading_to_round,
            StagesConstants.ROUND_STAGE: self.round,
            StagesConstants.ROUND_CLOSE: self.close_round,
            StagesConstants.EXIT_STAGE: self._close_game,
        }

        self.server_controller: ServerController = ServerController()
        self.client: Network = None

    def loading_to_round(self):
        try:
            self.server_controller.run_server()
            self.connect_to_server()
        except Exception as e:
            LOGGER.error(e)
            self.client = None
            self.stage_controller.set_main_menu_stage()

        else:
            self.stage_controller.set_round_stage()

    def connect_to_server(self):
        self.client = Network()
        response = self.client.connect()
        if self.client.connected:
            LOGGER.info('Client connected')
        #  start_new_thread(self.__round_recv_thread, ())
        else:
            self.client = None
            raise ConnectionError(response.get(NetworkKeys.ServerMessages, ''))

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
        LOGGER.info(f'Started RECV thread.')
        self.stage_controller.set_round_stage()

        while self.client.connected:
            try:
                recv = self.client.receive()
                LOGGER.info(f'Thread {recv}')
            except Exception as e:
                LOGGER.error(e)

    def round(self):
        request_data = {}
        ROUND_STAGE_LOGIC.update(request_data)
        ROUND_STAGE_LOGIC.draw()

        if request_data:
            self.client.send(request_data)

    def close_round(self):
        if self.server_controller:
            self.server_controller.stop_server()
        if self.client:
            self.client.disconnect()

        self.stage_controller.set_main_menu_stage()

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
