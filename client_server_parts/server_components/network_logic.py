import traceback
from time import sleep
from _thread import start_new_thread
from common.logger import Logger
from constants.network_keys import *
from settings.network import *
from client_server_parts.server_components.player_connection_handler import ConnectionHandler
from game_logic.components.player_object import Player
from client_server_parts.server_components.config import ServerConfig

LOGGER = Logger()


class NetworkLogic:
    TIME_WITHOUT_CONNECTION = 180

    def __init__(self, server):
        self.server = server
        self.config: ServerConfig = server.config

        self.json_to_str = server.json_to_str
        self.str_to_json = server.str_to_json

        self.socket_opened = 0
        self.do_not_accept_connections = 0
        self.socket = None
        self.connected_players_count = 0
        self.player_connected_in_past = set()
        self.players_data: {str: Player} = server.players_data
        self.server_actions = {}
        self.addresses_ban_list = []
        self.token_ban_list = set()

        self.players_connections: {str: ConnectionHandler} = server.players_connections  # token: socket connection

        self.address = socket.gethostbyname(socket.gethostname())

        self.open_connection()
        self.start()

    def open_connection(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.address, self.config.server_port))
            self.socket.listen()
            self.socket_opened = 1
            self.do_not_accept_connections = 0

        except Exception as e:
            LOGGER.error(e)
            self.server.stop()
            raise e
        else:
            LOGGER.info('Connection successfully opened.')

    def start(self):
        try:
            start_new_thread(self.__connection_handling, ())
            LOGGER.info(f'Server started {self.address}:{self.config.server_port}')
        except Exception as e:
            LOGGER.info(f'Connection handler error.')
            LOGGER.error(e)
            self.server.stop()

    def __connection_handling(self):
        try:
            while self.socket_opened and self.server.alive:
                if self.do_not_accept_connections:
                    sleep(5)
                    continue
                sleep(0.5)
                LOGGER.info('Waiting for connection')
                try:
                    player_connection, (addr, port) = self.socket.accept()
                    # LOGGER.info(f'Connection accepted {addr}:{port}')
                    LOGGER.info(f'Connection accepted :{port}')
                    player_connection = ConnectionHandler(connection=player_connection)
                except Exception as e:
                    LOGGER.error(e)
                else:

                    client_data = self.str_to_json(player_connection.recv(2048).decode())
                    LOGGER.info(f'Client data: {client_data}')

                    # get player old key
                    player_token = client_data.get(PlayerAttrs.Token)

                    # if key was`t connected -> send new key
                    if player_token not in self.player_connected_in_past or player_token in self.players_connections:
                        pre_player_id = player_token
                        player_token = str(hash(str((addr, port))))
                        # if player was admin add new token as admin
                        if self.server.is_admin(pre_player_id) and pre_player_id not in self.players_connections:
                            self.server.add_admin(player_token)
                            self.server.remove_admin(pre_player_id)

                        LOGGER.info(f'New player id {player_token}')

                    player_connection.player_id = player_token

                    # self.players_data[player_token].ip = (addr, port)
                    try:
                        self.process_connection(player_token=player_token, addr=addr,
                                                player_connection=player_connection, client_data=client_data)
                    except Exception as e:
                        LOGGER.error(traceback.format_exc())
                        LOGGER.error(f'Failed to process connection {e}')
                        try:
                            self.players_data.pop(player_token)
                            server_response_data = {
                                ServerConnectAnswers.CONNECTION_ANSWER: ServerConnectAnswers.FailedToConnect,
                            }
                            player_connection.send(self.json_to_str(server_response_data))
                        except Exception:
                            pass
            else:
                LOGGER.info('STOPPED')
        except Exception as e:
            LOGGER.error(f'CONNECTION HANDLING ERROR')
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

        if client_data[NetworkKeys.Password] != self.config.game_password:
            self.send_bad_password(server_response_data, player_connection, client_data, addr)

        else:
            self.connect_as_player(server_response_data=server_response_data,
                                   player_connection=player_connection,
                                   player_token=player_token,
                                   client_data=client_data,
                                   addr=addr)

    def connect_as_player(self, server_response_data, player_connection, player_token, client_data, addr):
        LOGGER.info(f'Connecting {player_token} as player')

        self.player_connected_in_past.add(player_token)
        self.players_connections[player_token] = player_connection

        self.players_data[player_token] = Player(nickname=client_data.get(PlayerAttrs.Nickname),
                                                 token=player_token, addr=addr,
                                                 is_admin=self.server.is_admin(player_token),
                                                 number=self.connected_players_count+1,
                                                 )

        server_response_data[NetworkKeys.ServerAnswer] = 'Successfully connected.'
        server_response_data[NetworkKeys.Seed] = self.config.seed
        server_response_data[ServerConnectAnswers.CONNECTION_ANSWER] = ServerConnectAnswers.Connected
        server_response_data[SRC.OtherPlayers] = self.get_other_players_data(player_token)
        server_response_data[NetworkKeys.RoundStage] = self.server.current_stage
        server_response_data[PlayerAttrs.Token] = player_token
        server_response_data[PlayerAttrs.IsAdmin] = self.server.is_admin(player_token)
        server_response_data[PlayerUpdates.Data] = self.players_data[player_token].get_data_dict()

        if self.server.current_stage == NetworkKeys.RoundRoundStage:
            server_response_data[NetworkKeys.DetailsPool] = self.server.GAME_LOGIC.details_pool.get_dict()
            # TODO add default details for current player

        elif self.server.current_stage == NetworkKeys.RoundLobbyStage:
            self.server.LOBBY_LOGIC.new_player_connected(player_token)
            server_response_data[NetworkKeys.DetailsPoolSettings] = self.config.details_pool_settings
            server_response_data[NetworkKeys.DefaultDetailsSettings] = self.config.default_details_settings

        LOGGER.info(f'Sending response: {server_response_data}')
        player_connection.send(self.json_to_str(server_response_data))
        LOGGER.info(f'Successfully sent.')

        LOGGER.info(f'Connected. {player_token}.'
                    f' Player #{self.connected_players_count}.'
                    f' Nickname {client_data.get(PlayerAttrs.Nickname)}.')
        self.connected_players_count += 1

        self.server.start_player_thread(player_token)

    def get_other_players_data(self, token):
        d = {token: self.players_data[token_].get_data_dict() for token_ in self.players_connections if token != token_ and token_ in self.players_data}
        return d

    def reconnect_player(self, server_response_data, player_connection, player_token, client_data, addr):
        LOGGER.info(f'Player {player_token} is reconnecting.')
        if ServerActions.DELETE_PLAYER in self.server_actions:
            self.server_actions[ServerActions.DELETE_PLAYER].append(player_token)
        else:
            self.server_actions[ServerActions.DELETE_PLAYER] = [player_token, ]

        LOGGER.info(f'Reconnected. {player_token}.'
                    f' Player #{self.connected_players_count}.'
                    f' Nickname {client_data.get(PlayerAttrs.Nickname)}.'
                    f' Color: {client_data.get("player_color")}')

        server_response_data[ServerConnectAnswers.Connected] = True
        server_response_data[PlayerAttrs.Token] = player_token
        server_response_data[NetworkKeys.ServerAnswer] = 'Successfully reconnected.'

        self.players_data[player_token] = Player(nickname=client_data.get(PlayerAttrs.Nickname),
                                                 token=player_token, addr=addr) # TODO get old object
        self.players_connections[player_token] = player_connection
        self.player_connected_in_past.add(player_token)
        self.server.GAME_LOGIC.start_player_handling(player_token)

    def send_bad_password(self, server_response_data, player_connection, client_data, addr):
        server_response_data[NetworkKeys.ServerAnswer] = 'Failed to connect, bad password.'
        server_response_data[ServerConnectAnswers.Connected] = ServerConnectAnswers.WrongPassword
        LOGGER.info(f'Failed to connect. {anon_host(addr)}. Nickname {client_data.get(PlayerAttrs.Nickname)}')
        LOGGER.info(f'Bad password! {client_data[NetworkKeys.Password]} != {self.config.game_password}')

        player_connection.send(self.json_to_str(server_response_data))

    # def send_to_many_players(self, server_response_data, player_connection):
    #     player_connection.send(self.json_to_str(server_response_data))

    def send_ban_message(self, server_response_data, player_connection, token):
        try:
            server_response_data[NetworkKeys.ServerAnswer] = 'You Banned.'
            server_response_data[ServerConnectAnswers.Connected] = ServerConnectAnswers.Banned
            player_connection.send(self.json_to_str(server_response_data))
            player_connection.close()
        except Exception as e:
            LOGGER.warn(f'Failed to ban player: {token}')
            LOGGER.warn(f'{e}')

    def disconnect_all_players(self, msg_to_players='All players disconnected'):
        data_to_players = self.json_to_str({ServerResponseCategories.DisconnectAll: True,
                                            NetworkKeys.ServerAnswer: msg_to_players})

        for player_id, connection in self.players_connections.copy().items():
            try:
                connection.send(data_to_players)
            except Exception as e:
                LOGGER.exception(f'Failed to send data to {player_id} before disconnect.\n\n{e}')

        sleep(10)

        for player_id, connection in self.players_connections.copy().items():
            try:
                self.disconnect_player(player_id)
            except Exception as e:
                LOGGER.exception(f'Error while disconnecting {player_id}: \n\n{e}')

    def disconnect_player(self, player_id, ban_player=False):
        if ban_player:
            self.addresses_ban_list.append(self.players_data[player_id].addr)
            self.token_ban_list.add(player_id)

        try:
            self.players_connections.pop(player_id).close()

        except Exception as e:
            LOGGER.error(f"Failed to disconnect {player_id}: \n\t{e}")
        else:
            LOGGER.info(f'Player {player_id} disconnected successfully.')

        self.connected_players_count -= 1

    def stop(self):
        LOGGER.info('Disconnecting all players')
        self.disconnect_all_players(f'Server stopped. Players: {self.players_connections}')
        self.socket.close()
        self.socket_opened = 0
