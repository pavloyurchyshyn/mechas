import sys
import time

from common.logger import Logger

LOGGER = Logger('server_logs', 0, std_handler=0).LOGGER

from settings.global_parameters import SET_CLIENT_INSTANCE

SET_CLIENT_INSTANCE(0)

import traceback
import json

from _thread import *
from client_server_parts.server_components.config import ServerConfig
from client_server_parts.server_components.player_connection_handler import ConnectionHandler
from client_server_parts.server_components.game_logic import GameLogic
from client_server_parts.server_components.lobby_logic import LobbyLogic
from client_server_parts.server_components.network_logic import NetworkLogic
from constants.network_keys import NetworkKeys

TIMEOUT = 60


class Server:
    def __init__(self):
        self.alive = 1
        self.current_stage = NetworkKeys.RoundLobbyStage

        self.game_thread_id = None
        self.lobby_thread_id = None
        start_new_thread(self.timeout_check, ())

        self.config = ServerConfig()
        self.players_connections: {str: ConnectionHandler} = {}  # token: socket connection
        self.players_data = {}  # token: data obj

        self.GAME_LOGIC = GameLogic(self)
        self.LOBBY_LOGIC = LobbyLogic(self)

        self.network_logic = NetworkLogic(server=self)
        self.start_lobby_logic()
        # self.start_game_logic()
        self.start_game_logic_status_check()

    def switch_to_game(self):
        self.current_stage = NetworkKeys.RoundRoundStage
        self.start_game_logic()

    def timeout_check(self):
        LOGGER.info(f'Started timeout')
        finish = time.time() + TIMEOUT
        while finish > time.time():
            time.sleep(5)
            LOGGER.info(f'Time left {finish - time.time()} seconds')

        else:
            LOGGER.info(f'TIMEOUT')
            self.stop()

    def start_lobby_logic(self):
        LOGGER.info('Game LOBBY started')
        try:
            self.lobby_thread_id = start_new_thread(self.LOBBY_LOGIC.start_lobby, ())
        except Exception as e:
            LOGGER.error(e)
            self.stop()

    def start_game_logic(self):
        LOGGER.info('Game LOGIC started')
        try:
            self.game_thread_id = start_new_thread(self.GAME_LOGIC.run_game, ())
        except Exception as e:
            LOGGER.error(e)
            self.stop()

    def start_game_logic_status_check(self):
        LOGGER.info('Alive check started')
        while self.alive:
            self.alive = self.GAME_LOGIC.alive or self.LOBBY_LOGIC.alive
            time.sleep(10)
        LOGGER.info('Stopped')

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
            LOGGER.error(f'Failed to stop server_components. {e}')
            LOGGER.error(traceback.format_exc())
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
        Server()
    except Exception as e:
        LOGGER.critical(e)
        LOGGER.error('Final fail')
        LOGGER.error(traceback.format_exc())
        LOGGER.error(sys.exc_info()[2])
        raise Exception(e)
