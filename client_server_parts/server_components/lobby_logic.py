import re
import traceback
from _thread import start_new_thread
from time import sleep, time
from constants.network_keys import NetworkKeys, PlayerUpdates
from constants.network_keys import ServerResponseCategories, PlayerActions, CheckRegex, SRC, SLC
from common.logger import Logger
from client_server_parts.server_components.mixins.message_processor import MessageProcessorMixin as MPM
from client_server_parts.server_components.functions.request_normalizer import normalize_request

LOGGER = Logger('server_logs', 0, std_handler=0).LOGGER


class LobbyLogic(MPM, ):
    def __init__(self, server):
        self.config = server.config
        self.server = server
        self.players_connections = server.players_connections
        self.players_data: dict = server.players_data

        self.json_to_str = server.json_to_str
        self.str_to_json = server.str_to_json
        self.alive = True

        self.data_to_send = {}
        self.start_lobby()

    def new_player_connected(self, token):
        self.data_to_send[SRC.NewPlayers] = self.data_to_send.get(SRC.NewPlayers, {})
        self.data_to_send[SRC.NewPlayers][token] = self.players_data[token].get_data_dict()

    def start_player_thread(self, server, player_token):
        start_new_thread(self.__player_thread, (server, player_token))

    def __player_thread(self, server, player_token):
        try:
            connection = server.get_connection(player_token)

            while self.server.current_stage == NetworkKeys.RoundLobbyStage:
                player_request = connection.recv().decode()
                if player_request and player_request != '{}':
                    player_request = normalize_request(player_request)
                    player_request = self.str_to_json(player_request)
                    LOGGER.info(f'Received {player_token}: {player_request}')
                    self.__process_received(player_token, player_request)

        except Exception as e:
            if player_token in self.server.players_connections:
                LOGGER.error(e)
                LOGGER.error(traceback.format_exc())
                server.disconnect_player(player_token)
                self.data_to_send[SLC.KickPlayer] = player_token
                if self.server.is_admin(player_token):
                    self.server.stop()
            else:
                LOGGER.info(f'Player {player_token} was disconnected, thread stopped.')

    def __process_received(self, player_token, player_request):
        player = self.players_data[player_token]
        self.process_messages(player_token, player_request)
        self.__process_kicks(player_token, player_request)

    def __process_kicks(self, player_token, player_request):
        if SLC.KickPlayer in player_request and self.server.is_admin(player_token):
            LOGGER.info(f'{player_token} kicking {player_request[SLC.KickPlayer]}')
            self.server.disconnect_player(player_request[SLC.KickPlayer])
            self.data_to_send[SLC.KickPlayer] = player_request[SLC.KickPlayer]
            p_obj = self.players_data.pop(player_request[SLC.KickPlayer])
            self.send_bare_message(f'Kicking {p_obj.nickname}')

    def start_lobby(self):
        start_new_thread(self.__start_lobby, ())

    def __start_lobby(self):
        LOGGER.info('Sever Lobby loop started.')
        update_delay = 1 / 32
        LOGGER.info(f'Tick rate {64}. Time per frame: {update_delay}')

        try:
            while self.server.alive and self.server.current_stage == NetworkKeys.RoundLobbyStage:
                t = time()
                self.update()
                sl = update_delay - (time() - t)
                # LOGGER.info(f'Time spent for calculation {time() - t}, sleep {sl}')
                if sl > 0:
                    sleep(sl)
        except Exception as e:
            LOGGER.critical('Lobby loop stopped.')
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
        finally:
            self.server.alive = False
            self.alive = False
            LOGGER.info('Stopped lobby stage')

    def update(self):
        if self.data_to_send:
            data = self.data_to_send.copy()
            self.data_to_send.clear()
            self.send_data(data)

    def send_data(self, data):
        if data.get('players_updates'):
            LOGGER.info(f'Sending: {data}')
        for token, conn in self.players_connections.copy().items():
            conn.send(self.json_to_str(data))
