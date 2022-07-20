from constants.server.network_keys import NetworkKeys
from constants.server.network_keys import SRC, SLC
from common.logger import Logger
from client_server_parts.server_components.mixins.message_processor import MessageProcessorMixin as MPM

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

    def new_player_connected(self, token):
        self.data_to_send[SRC.NewPlayers] = self.data_to_send.get(SRC.NewPlayers, {})
        self.data_to_send[SRC.NewPlayers][token] = self.players_data[token].get_data_dict()

    def process_received(self, player_token, player_request):
        player = self.players_data[player_token]
        self.process_messages(player_token, player_request)
        self.__process_kicks(player_token, player_request)
        self.__process_game_start(player_token, player_request)

    def __process_game_start(self, player_token: str, player_request: dict):
        if player_request.get(SLC.StartGame, False) and self.server.is_admin(player_token):
            LOGGER.info(f'Game stage started')
            self.alive = False
            self.server.GAME_LOGIC.build_round()
            self.data_to_send[NetworkKeys.SwitchRoundStageTo] = NetworkKeys.RoundRoundStage
            self.data_to_send[NetworkKeys.DetailsPool] = self.server.GAME_LOGIC.details_pool.get_dict()
            self.update()
            self.server.switch_to_game()

    def __process_kicks(self, player_token, player_request):
        if SLC.KickPlayer in player_request and self.server.is_admin(player_token):
            LOGGER.info(f'{player_token} kicking {player_request[SLC.KickPlayer]}')
            self.server.disconnect_player(player_request[SLC.KickPlayer])
            self.data_to_send[SLC.KickPlayer] = player_request[SLC.KickPlayer]
            p_obj = self.players_data.pop(player_request[SLC.KickPlayer])
            self.send_bare_message(f'Kicking {p_obj.nickname}')

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
