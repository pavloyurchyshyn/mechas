import re
import traceback
from _thread import start_new_thread

from stages.round.page import Round

from common.logger import Logger
from common.stages import Stages
from common.global_clock import ROUND_CLOCK
from network.client.client_network import Network
from network.server.server_controller import ServerController

from constants.network_keys import NetworkKeys
from constants.network_keys import ServerResponseCategories, CheckRegex

from game_logic.player_object import Player
from mechas.base.mech import BaseMech
LOGGER = Logger().LOGGER


class RoundRelatedLogic:
    FEW_RECV_SYMBOL = '}{'

    def __init__(self):
        self.stage_controller = Stages()
        self.round_ui: Round = None
        self.server_controller: ServerController = ServerController()
        self.client: Network = None

    def host_and_connect(self):
        try:
            self.server_controller.run_server()
        except Exception as e:
            LOGGER.error(e)
            self.client = None
            self.stage_controller.set_close_round_stage()

        else:
            self.stage_controller.set_connect_stage()

    def connect_to_server(self):
        try:
            self.round_ui = Round()
            self.client = Network()
            response = self.client.connect()
            if self.client.connected:
                self.round_ui.set_player(Player(self.client.token, {}, BaseMech((1, 1))))
                LOGGER.info('Client connected')
                start_new_thread(self.__round_recv_thread, ())
                self.stage_controller.set_round_stage()

            else:
                self.client = None
                raise ConnectionError(response.get(NetworkKeys.ServerMessages, ''))

        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
            self.client = None
            self.stage_controller.set_close_round_stage()

        else:
            self.stage_controller.set_round_stage()

    def round(self):
        self.round_ui.update()
        self.round_ui.draw()

        if self.round_ui.player_response:
            # LOGGER.info(f"Player response: {self.round_ui.player_response}")
            self.client.send(self.round_ui.player_response)
            self.round_ui.player_response.clear()

        if not self.client.connected:
            self.stage_controller.set_close_round_stage()

    def close_round(self):
        self.round_ui = None
        if self.server_controller:
            self.server_controller.stop_server()
        if self.client:
            self.client.disconnect()

        self.stage_controller.set_main_menu_stage()

    # ===========================================
    def __round_recv_thread(self):
        LOGGER.info(f'Started RECV thread.')

        while self.client.connected:
            try:
                recv = self.__normalize_recv(self.client.receive())
                self.__process_received_data(recv)
            except Exception as e:
                LOGGER.error(e)
                LOGGER.error(traceback.format_exc())
                self.client.disconnect()

    def __normalize_recv(self, recv):
        if self.FEW_RECV_SYMBOL in recv and not re.search(CheckRegex.good_recv_re, recv):
            recv: str = recv.split(self.FEW_RECV_SYMBOL)[-1]
            recv = recv if recv.startswith('{') else '{' + recv

        return self.client.str_to_json(recv)

    def __process_received_data(self, data: dict):
        if data:
            if len(data) > 1:
                LOGGER.info(f'Received data: {data}')
            self.__update_time(data)
            self.round_ui.process_server_data(data)

    def __update_time(self, data: dict):
        if ServerResponseCategories.MatchTime in data:
            ROUND_CLOCK.set_time(*data.pop(ServerResponseCategories.MatchTime))
