import time

from common.logger import Logger

LOGGER = Logger('server_logs', 0, std_handler=0).LOGGER

from settings.global_parameters import SET_CLIENT_INSTANCE

SET_CLIENT_INSTANCE(0)

from settings.network import *
import socket
from _thread import *
import traceback
from argparse import ArgumentParser
import json
from constants.network_keys import *
from network.server.player_connection_handler import ConnectionHandler
from time import sleep, time
import sys


class Server:
    TIME_WITHOUT_CONNECTION = 180

    def __init__(self):
        self.address = socket.gethostbyname(socket.gethostname())
        self.parse_arguments()

        self.number_of_connected_players = 0

        self.players_connections: {str: ConnectionHandler} = {}  # token: socket connection
        self.player_id_to_ip = {}
        self.player_connected_in_past = set()  # for disconnected players
        self.players_names = {}  # token: name
        self.players_simple_data = {}
        self.players_objects = {}

        self.server_actions = {}

        self.ban_list = []
        self.addresses_ban_list = []

        self.alive = 1

        self.open_connection()
        self.start_connection_handling()
        # self.start_game_logic()
        self.start_game_logic_status_check()

    def start_game_logic(self):
        LOGGER.info('Game logic started')
        try:
            self.game_thread_id = start_new_thread(self.GAME_LOGIC.run_game, ())
        except Exception as e:
            LOGGER.error(e)
            self.stop()

    def start_game_logic_status_check(self):
        LOGGER.info('Alive check started')
        LOGGER.info('Sever Game loop started.')
        update_delay = 1 / 64
        LOGGER.info(f'Tick rate {64}. Time per frame: {update_delay}')

        finish = time() + 10
        while self.alive:
            t = time()
            for token, conn in self.players_connections.items():
                response = conn.recv()
                if response:
                    LOGGER.info(f'{token}: {response}')
                conn.send(self.json_to_str({'all_ok': True}))

            if time() > finish:
                self.alive = False
                LOGGER.info(f'Timeout')
            sl = update_delay - (time() - t)
            # LOGGER.info(f'Time spent for calculation {time() - t}, sleep {sl}')
            if sl > 0:
                sleep(sl)
        LOGGER.info('Stopped')

    def start_connection_handling(self):
        start_new_thread(self.__connection_handling, ())
        LOGGER.info(f'Server started {self.address}:{self.server_port}')

    def __connection_handling(self):
        try:
            while self.socket_opened and self.alive:
                if self.do_not_accept_connections:
                    sleep(5)
                    continue
                sleep(0.5)
                LOGGER.info('Waiting for connection')
                try:
                    player_connection, (addr, port) = self.socket.accept()
                    LOGGER.info(f'Connection accepted {addr}:{port}')
                    player_connection = ConnectionHandler(connection=player_connection)
                except Exception as e:
                    LOGGER.error(e)
                else:

                    client_data = self.str_to_json(player_connection.recv(2048).decode())
                    LOGGER.info(f'Client data: {client_data}')

                    # get player old key
                    player_token = client_data.get(PlayerAttrs.Token)

                    # if key was`t connected -> send new key
                    if player_token not in self.player_connected_in_past:
                        pre_player_id = player_token
                        player_token = str(hash(str((addr, port))))
                        # if player was admin add new token as admin
                        if self.is_admin(pre_player_id):
                            self.add_admin(player_token)
                            self.remove_admin(pre_player_id)
                        LOGGER.info(f'New player id {player_token}')

                    player_connection.player_id = player_token

                    self.player_id_to_ip[player_token] = (addr, port)
                    try:
                        self.process_connection(player_token=player_token, addr=addr,
                                                player_connection=player_connection, client_data=client_data)
                    except Exception as e:
                        LOGGER.error(f'Failed to process connection {e}')
                        try:
                            self.player_id_to_ip.pop(player_token)
                            server_response_data = {
                                ServerConnectAnswers.CONNECTION_ANSWER: ServerConnectAnswers.FailedToConnect,
                            }
                            player_connection.send(self.json_to_str(server_response_data))
                        except Exception:
                            pass

        except Exception as e:
            LOGGER.error(e)
            self.alive = 0

    def process_connection(self, player_token, addr, player_connection, client_data):
        server_response_data = {
            ServerConnectAnswers.CONNECTION_ANSWER: ServerConnectAnswers.FailedToConnect,
        }

        # if player_token in self.ban_list or addr in self.addresses_ban_list:
        #     self.send_ban_message(server_response_data, player_connection)
        #
        # elif player_token in self.player_connected_in_past:
        #     self.reconnect_player(server_response_data=server_response_data,
        #                           player_connection=player_connection,
        #                           player_id=player_token,
        #                           client_data=client_data)
        #
        # elif self.number_of_connected_players >= self.max_number_of_players:
        #     self.send_to_many_players(server_response_data, player_connection)

        if client_data[NetworkKeys.Password] != self.game_password:
            self.send_bad_password(server_response_data, player_connection, client_data, addr)

        else:
            self.connect_as_player(server_response_data=server_response_data,
                                   player_connection=player_connection,
                                   player_token=player_token,
                                   client_data=client_data)

    def connect_as_player(self, server_response_data, player_connection, player_token, client_data):
        LOGGER.info(f'Connecting {player_token} as player')
        self.player_connected_in_past.add(player_token)
        nickname = client_data[PlayerAttrs.Nickname]  # self.get_nickname(client_data[NICKNAME], player_hash=player_id)

        self.players_names[player_token] = nickname
        self.players_connections[player_token] = player_connection

        self.players_simple_data[player_token] = {PlayerAttrs.Nickname: nickname
                                                  }
        server_response_data[NetworkKeys.ServerAnswer] = 'Successfully connected.'
        server_response_data[ServerConnectAnswers.CONNECTION_ANSWER] = ServerConnectAnswers.Connected
        server_response_data[PlayerAttrs.Token] = player_token

        LOGGER.info(f'Sending')
        player_connection.send(self.json_to_str(server_response_data))
        LOGGER.info(f'Successfully sent {server_response_data}')

        LOGGER.info(f'Connected. {player_token}.'
                    f' Player #{self.number_of_connected_players}.'
                    f' Nickname {nickname}.')
        self.number_of_connected_players += 1

    def reconnect_player(self, server_response_data, player_connection, player_token, client_data):
        LOGGER.info(f'Player {player_token} is reconnecting.')
        if ServerActions.DELETE_PLAYER in self.server_actions:
            self.server_actions[ServerActions.DELETE_PLAYER].append(player_token)
        else:
            self.server_actions[ServerActions.DELETE_PLAYER] = [player_token, ]

        nickname = client_data[PlayerAttrs.Nickname]
        LOGGER.info(f'Reconnected. {player_token}.'
                    f' Player #{self.number_of_connected_players}.'
                    f' Nickname {nickname}.'
                    f' Color: {client_data.get("player_color")}')

        server_response_data[ServerConnectAnswers.Connected] = True
        server_response_data[PlayerAttrs.Token] = player_token
        server_response_data[NetworkKeys.ServerAnswer] = 'Successfully reconnected.'

        self.players_simple_data[player_token] = {
            PlayerAttrs.Nickname: nickname,
        }
        self.players_connections[player_token] = player_connection
        self.player_connected_in_past.add(player_token)

    def send_bad_password(self, server_response_data, player_connection, client_data, addr):
        server_response_data[NetworkKeys.ServerAnswer] = 'Failed to connect, bad password.'
        server_response_data[ServerConnectAnswers.Connected] = ServerConnectAnswers.WrongPassword
        LOGGER.info(f'Failed to connect. {anon_host(addr)}. Nickname {client_data[PlayerAttrs.Nickname]}')
        LOGGER.info(f'Bad password! {client_data[NetworkKeys.Password]} != {self.game_password}')

        player_connection.send(self.json_to_str(server_response_data))

    def send_to_many_players(self, server_response_data, player_connection):
        player_connection.send(self.json_to_str(server_response_data))

    def send_ban_message(self, server_response_data, player_connection):
        server_response_data[NetworkKeys.ServerAnswer] = 'You Banned.'
        server_response_data[ServerConnectAnswers.Connected] = ServerConnectAnswers.Banned
        player_connection.send(self.json_to_str(server_response_data))
        player_connection.close()

    def disconnect_all_players(self, msg_to_players='All players disconnected'):
        data_to_players = self.json_to_str({ServerResponseCategories.DisconnectAll: True,
                                            NetworkKeys.ServerAnswer: msg_to_players})

        for player_id, connection in self.players_connections.copy().items():
            try:
                connection.send(data_to_players)
            except Exception as e:
                LOGGER.exception(f'Failed to send data to {player_id} before disconnect.\n\n{e}')
            try:
                self.disconnect_player(player_id)
            except Exception as e:
                LOGGER.exception(f'Error while disconnecting {player_id}: \n\n{e}')

    def disconnect_player(self, player_id, ban_player=False):
        if ban_player:
            self.addresses_ban_list.append(self.player_id_to_ip[player_id])
            self.ban_list.append(player_id)

        try:
            self.players_connections.pop(player_id).close()

        except Exception as e:
            LOGGER.error(f"Failed to disconnect {player_id}: \n\t{e}")
        else:
            LOGGER.info(f'Player {player_id} disconnected successfully.')

        self.number_of_connected_players -= 1

    def is_admin(self, player_id):
        return player_id in self.admins_list

    def remove_admin(self, player_id):
        self.admins_list.remove(player_id)

    def add_admin(self, player_id):
        self.admins_list.add(player_id)

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

    def open_connection(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.address, self.server_port))
            self.socket.listen()
            self.socket_opened = 1
            self.do_not_accept_connections = 0
        except Exception as e:
            LOGGER.error(e)
            self.stop()
            raise e
        else:
            LOGGER.info('Connection successfully opened.')

    def parse_arguments(self):
        arg_parser = ArgumentParser()

        for argument, value in SERVER_ARGUMENTS.items():
            arg_parser.add_argument(argument, default=value[0], help=value[1])

        arguments = arg_parser.parse_args()
        LOGGER.info(arguments.__dict__)

        self.max_number_of_players = 10
        self.game_password = arguments.password
        self.server_port = int(arguments.port)
        self.main_admin_key = str(arguments.admin_token) if arguments.admin_token != 'None' else '_'
        self.admins_list = set(filter(bool, self.main_admin_key.split(',')))

        self.admins_list.add(self.main_admin_key)

    def stop(self):
        self.alive = False
        LOGGER.info('Stopping server')
        LOGGER.info('Disconnecting all players')
        self.disconnect_all_players(f'Server stopped. Players: {self.players_connections}')
        try:
            self.socket.close()
            self.socket_opened = 0
            # self.stop_game_processor()

        except Exception as e:
            LOGGER.error(f'Failed to stop server. {e}')

        # try:
        #     self.GAME_LOGIC.alive = 0
        # except Exception as e:
        #     LOGGER.error(e)
        # else:
        #     LOGGER.info('Game logic stopped.')


if __name__ == '__main__':
    try:
        LOGGER.info(f'Start')
        Server()
    except Exception as e:
        LOGGER.critical(e)
        LOGGER.error('Final fail')
        LOGGER.error(traceback.format_exc())
        LOGGER.error(sys.exc_info()[2])
        raise Exception(e)
