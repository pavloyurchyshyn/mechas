import re
import traceback
from _thread import start_new_thread

from stages.play_stage.round_stage.page import Round
from stages.play_stage.round_lobby_stage.page import LobbyWindow

from common.logger import Logger
from common.stages import Stages

from client_server_parts.client.client_network import Network
from client_server_parts.server_controller import ServerController

from constants.server.network_keys import NetworkKeys, PlayerUpdates, PlayerAttrs
from constants.server.network_keys import ServerResponseCategories

from game_logic.components.player_object import Player
from game_logic.components.pools.details_pool import DetailsPool
from game_logic.components.pools.skills_pool import SkillsPool

from visual.UIController import UI_TREE

from mechas.base.mech import BaseMech

LOGGER = Logger()


class RoundStages:
    Lobby = 'lobby'


class RoundRelatedLogic:
    FEW_RECV_SYMBOL = '}{'

    def __init__(self):
        self.stage_controller = Stages()
        self.server_controller: ServerController = ServerController()
        self.round_stage = NetworkKeys.RoundLobbyStage

        self.round_ui: Round = None
        self.lobby_ui: LobbyWindow = None
        self.client: Network = None

        self.skills_pool: SkillsPool = None
        self.details_pool: DetailsPool = None
        self.details_pool_settings: dict = {}

        self.update_method = None
        self.process_received_data = None

        self.this_player: Player = None
        self.other_players = {}

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
            self.client = Network()
            LOGGER.info(f'Connecting.')
            response = self.client.connect()

            if self.client.connected:
                LOGGER.info(f'Client connected: {response}')
                self.this_player = Player(**response.get(PlayerUpdates.Data, {}))
                LOGGER.info(f'This player: {self.this_player.get_data_dict()}')

                self.process_connection_data(response)

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

    def process_connection_data(self, response):
        self.round_stage = response[NetworkKeys.RoundStage]
        self.skills_pool: SkillsPool = SkillsPool()
        self.details_pool: DetailsPool = DetailsPool(self.skills_pool, seed=response[NetworkKeys.Seed])
        # TODO make a different stages
        self.details_pool_settings.clear()

        for token, data in response.get(ServerResponseCategories.OtherPlayers, {}).items():
            LOGGER.info(f'Added new player: {token} - {data}')
            self.other_players[token] = Player(**data)

        if self.round_stage == NetworkKeys.RoundLobbyStage:
            self.details_pool_settings.update(response[NetworkKeys.DetailsPoolSettings])
            self.build_lobby_menu(response)

        elif self.round_stage == NetworkKeys.RoundRoundStage:
            self.build_round(response)

    def build_lobby_menu(self, response):
        self.lobby_ui = LobbyWindow(response, player=self.this_player, round_logic=self)
        self.lobby_ui.players_window.add_player(self.this_player)
        for obj in self.other_players.values():
            self.lobby_ui.players_window.add_player(obj)

        self.update_method = self.lobby_update
        self.process_received_data = self.__process_received_data_lobby

    def build_round(self, response):
        LOGGER.info(f'Build round: {response}')
        try:
            self.this_player.mech = self.build_mech(response)

            self.details_pool.load_details_list(response[NetworkKeys.DetailsPool])

            self.round_ui = Round(self.this_player, self.other_players, response[NetworkKeys.PlayersNumber])
            self.round_ui.mech_window.calculate_side_positions()

            self.process_received_data = self.__process_received_data_round
            self.update_method = self.round_update

        except Exception as e:
            LOGGER.error(f'Failed to build round: {e}')

    # ------------- UPDATE METHODS -------------------
    def update(self):
        if self.update_method:
            self.update_method()

    def lobby_update(self):
        self.lobby_ui.update()
        self.lobby_ui.draw()
        if self.lobby_ui.player_response:
            # LOGGER.info(f"Player response: {self.round_ui.player_response}")
            self.client.send(self.lobby_ui.player_response)
            self.lobby_ui.player_response.clear()

    def round_update(self):
        self.round_ui.update()
        self.round_ui.draw()

        if self.round_ui.player_response:
            # LOGGER.info(f"Player response: {self.round_ui.player_response}")
            self.client.send(self.round_ui.player_response)
            self.round_ui.player_response.clear()

        # if not self.client.connected:
        #     self.stage_controller.set_close_round_stage()

    # -----------------------------------------------------------

    def build_mech(self, response):
        this_player = response.get(ServerResponseCategories.PlayersUpdates).get(self.this_player.token)
        default_details = this_player.get(PlayerAttrs.DefaultDetails)
        def_details = [self.details_pool.get_detail_by_id(d_id) for d_id in default_details]
        self.this_player.default_details = def_details
        return BaseMech(this_player.get(PlayerAttrs.Position, (5, 5)), )

    def close_round(self):
        if self.client:
            self.client.disconnect()
        if self.server_controller:
            self.server_controller.stop_server()

        if self.lobby_ui:
            self.lobby_ui = None

        if self.round_ui:
            UI_TREE.delete_menu(self.round_ui.name)

        self.round_ui = None
        self.this_player: Player = None
        self.other_players.clear()
        self.details_pool_settings.clear()
        self.stage_controller.set_main_menu_stage()
        self.skills_pool: SkillsPool = None
        self.details_pool: DetailsPool = None
        self.update_method = None
        self.process_received_data = None

    # ===========================================
    def __round_recv_thread(self):
        LOGGER.info(f'Started RECV thread.')

        while self.client.connected:
            try:
                # recv = self.__normalize_recv(self.client.receive())
                recvs = self.client.bulk_receive()
                for recv in recvs:
                    self.__process_received_data(self.client.str_to_json(recv))
            except Exception as e:
                LOGGER.error(e)
                LOGGER.error(traceback.format_exc())
                self.client.disconnect()
                self.stage_controller.set_close_round_stage()

    def __process_received_data(self, data: dict):
        self.__check_for_stage_switch(data)

        self.process_received_data(data)

        self.__check_for_disconnect(data)

    def __check_for_stage_switch(self, data):
        if NetworkKeys.SwitchRoundStageTo in data:
            new = data.get(NetworkKeys.SwitchRoundStageTo)
            LOGGER.info(f'Switch to {new}')
            if new != self.round_stage:
                self.round_stage = new
                LOGGER.info(f'Switch to {new} != {self.round_stage}')
                LOGGER.info(f'Round UI {self.round_ui}')

                if self.round_stage == NetworkKeys.RoundRoundStage and self.round_ui is None:
                    self.build_round(data)
                    LOGGER.info(f'New update method: {self.round_update}')

    def __process_received_data_lobby(self, data):
        if data:
            LOGGER.info(f'Received data: {data}')
            self.lobby_ui.process_server_data(data)

    def __process_received_data_round(self, data):
        if data:
            if len(data) > 2:
                LOGGER.info(f'Received data: {data}')

            self.round_ui.process_server_data(data)

    def __check_for_disconnect(self, response):
        if response.get(ServerResponseCategories.DisconnectAll):
            self.client.disconnect()
            LOGGER.info(f'Got disconnect signal')
            self.stage_controller.set_close_round_stage()
