import sys
import time

from common.global_clock import ROUND_CLOCK
from common.logger import Logger

LOGGER = Logger('server_logs', 0, std_handler=0).LOGGER

from settings.global_parameters import SET_CLIENT_INSTANCE

SET_CLIENT_INSTANCE(0)

import traceback
import json

from _thread import *
from client_server_parts.server_components.config import ServerConfig
from client_server_parts.server_components.player_connection_handler import ConnectionHandler
from client_server_parts.game_logic.game_logic import GameLogic
from client_server_parts.server_components.lobby_logic import LobbyLogic
from client_server_parts.server_components.network_logic import NetworkLogic
from constants.server.network_keys import NetworkKeys
from client_server_parts.server_components.functions.request_normalizer import normalize_request

TIMEOUT = 30#90
TICK_RATE = 16


class Server:
    def __init__(self):
        self.alive = 1
        self.data_to_send = {}
        self.current_stage = NetworkKeys.RoundLobbyStage

        start_new_thread(self.timeout_check, ())

        self.config = ServerConfig()
        self.players_connections: {str: ConnectionHandler} = {}  # token: socket connection
        self.players_data = {}  # token: data obj

        self.GAME_LOGIC = GameLogic(self)
        self.LOBBY_LOGIC = LobbyLogic(self)
        self.process_received_method = self.LOBBY_LOGIC.process_received
        self.update_method = self.LOBBY_LOGIC.update

        self.network_logic = NetworkLogic(server=self)
        start_new_thread(self.start_game_logic_status_check, ())
        self.start()

    def start(self):
        LOGGER.info('Sever Lobby loop started.')
        update_delay = 1 / TICK_RATE
        LOGGER.info(f'Tick rate {TICK_RATE}. Time per frame: {update_delay}')
        LOGGER.info(f'Current stage: {self.current_stage}')
        LOGGER.info(f'Update method: {self.update_method}')
        ROUND_CLOCK.set_time(-999)
        try:
            while self.alive:
                t = time.time()
                self.update_method()
                sl = update_delay - (time.time() - t)
                # LOGGER.info(f'Time spent for calculation {time() - t}, sleep {sl}')
                if sl > 0:
                    time.sleep(sl)
                ROUND_CLOCK.update(time.time() - t)

        except Exception as e:
            LOGGER.critical('Lobby loop stopped.')
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
        finally:
            self.disconnect_all_players()
            self.alive = False
            LOGGER.info('Stopped lobby stage')

    def start_player_thread(self, token):
        start_new_thread(self.__player_thread, (token,))

    def __player_thread(self, token):
        connection = self.get_connection(token)
        LOGGER.info(f'Thread started: {token}')
        try:
            while self.alive:
                player_request = connection.recv().decode()
                if player_request and player_request != '{}':
                    player_request = normalize_request(player_request)
                    player_request = self.str_to_json(player_request)
                    LOGGER.info(f'Received {token}: {player_request}')
                    self.process_received(token, player_request)

        except Exception as e:
            if token in self.players_connections:
                LOGGER.error(e)
                LOGGER.error(traceback.format_exc())
                # self.disconnect_player(token)
                # self.data_to_send[SLC.KickPlayer] = player_token
                if self.is_admin(token):
                    LOGGER.info('Admin disconnected, stopping server.')
                    self.stop()
            else:
                LOGGER.info(f'Player {token} was disconnected, thread stopped.')
            LOGGER.info(f"Player {token} thread stopped.")

    def process_received(self, token, request):
        self.process_received_method(token, request)

    def switch_to_game(self):
        LOGGER.info(f'Switching to game ')
        ROUND_CLOCK.set_time(-30)
        self.current_stage = NetworkKeys.RoundRoundStage
        self.process_received_method = self.GAME_LOGIC.process_received
        self.GAME_LOGIC.build_round()
        self.update_method = self.GAME_LOGIC.update

    def timeout_check(self):
        LOGGER.info(f'Started timeout')
        finish = time.time() + TIMEOUT
        while finish > time.time():
            time.sleep(5)
            LOGGER.info(f'Time left {finish - time.time()} seconds')

        else:
            LOGGER.info(f'TIMEOUT')
            self.stop()

    def start_game_logic_status_check(self):
        LOGGER.info('Alive check started')
        while self.alive:
            self.alive = self.GAME_LOGIC.alive or self.LOBBY_LOGIC.alive
            time.sleep(10)
        LOGGER.info('status check stopped')

    def disconnect_all_players(self, msg_to_players='All players disconnected'):
        self.network_logic.disconnect_all_players(msg_to_players=msg_to_players)

    def disconnect_player(self, player_id, ban_player=False):
        self.network_logic.disconnect_player(player_id=player_id, ban_player=ban_player)

    def is_admin(self, player_id):
        return player_id in self.config.admins_list

    def remove_admin(self, player_id):
        self.config.admins_list.remove(player_id)

    def add_admin(self, player_id):
        self.config.admins_list.add(player_id)

    @staticmethod
    def str_to_json(string):
        if not string:
            return {}
        try:
            return json.loads(string)
        except Exception as e:
            LOGGER.error(f"String to json ->{string}<-: \n\t{e}")
            raise Exception(e)

    @staticmethod
    def json_to_str(json_):
        return json.dumps(json_).encode()

    def stop(self):
        self.alive = False
        LOGGER.info('Stopping server components')
        try:
            self.network_logic.stop()
        except Exception as e:
            LOGGER.error(f'Failed to stop network_logic. {e}')
        try:
            self.GAME_LOGIC.alive = 0
        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
        else:
            LOGGER.info('Game logic stopped.')

    def get_connection(self, player_token):
        return self.network_logic.players_connections.get(player_token)


if __name__ == '__main__':
    try:
        server = Server()
    except Exception as e:
        try:
            server.alive = False
        except:
            pass
        LOGGER.critical(e)
        LOGGER.error('Final fail')
        LOGGER.error(traceback.format_exc())
        LOGGER.error(sys.exc_info()[2])
        raise Exception(e)
