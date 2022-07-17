import traceback
import re
from _thread import start_new_thread
from time import sleep, time
from constants.network_keys import ServerResponseCategories, PlayerActions, CheckRegex, SRC
from common.logger import Logger
from common.global_clock import ROUND_CLOCK
from game_logic.components.pools.skills_pool import SkillsPool
from game_logic.components.pools.details_pool import DetailsPool
from game_logic.components.pools.pools_generator import PoolGenerator
from client_server_parts.server_components.config import ServerConfig
from client_server_parts.server_components.mixins.message_processor import MessageProcessorMixin
from client_server_parts.server_components.functions.request_normalizer import normalize_request
LOGGER = Logger('server_logs', 0, std_handler=0).LOGGER

TIMEOUT = 45


class GameLogic(MessageProcessorMixin, ):
    def __init__(self, server):
        self.server = server
        self.config: ServerConfig = self.server.config

        self.players_connections: dict = server.players_connections
        self.players_data: dict = server.players_data

        self.json_to_str = server.json_to_str
        self.str_to_json = server.str_to_json
        self.alive = True

        self.data_to_send = {}

        self.skills_pool: SkillsPool = None
        self.details_pool: DetailsPool = None

    def build_round(self):
        self.skills_pool = SkillsPool()
        self.details_pool = DetailsPool(self.skills_pool)  # TODO

        pool_generator = PoolGenerator(self.config.max_players_num, self.config.details_pool_settings)
        self.details_pool.load_details_list(pool_generator.get_details_list())

    def update(self):
        self.update_data_to_send()
        self.timeout()
        data = self.data_to_send.copy()
        self.data_to_send.clear()
        self.send_data(data)

    def timeout(self):
        if ROUND_CLOCK.time > 0:
            self.send_bare_message('Round timer end')
            ROUND_CLOCK.set_time(-30)

    def update_data_to_send(self):
        self.data_to_send[ServerResponseCategories.MatchTime] = ROUND_CLOCK()

    def process_received(self, token, player_request: dict):
        self.data_to_send[SRC.PlayersUpdates] = self.data_to_send.get(SRC.PlayersUpdates, {})
        player_update = self.data_to_send[SRC.PlayersUpdates][token] = self.data_to_send[SRC.PlayersUpdates].get(token, {})
        self.process_messages(token, player_request)
        self.process_ready_status(player_update, token, player_request)

    def process_ready_status(self, player_update, token, data):
        if PlayerActions.READY_STATUS in data:
            ready = data.pop(PlayerActions.READY_STATUS)
            player_update[ServerResponseCategories.ReadyState] = ready
            LOGGER.info(f'{token} ready status: {ready}')

    def send_data(self, data):
        # if data.get('players_updates'):
        LOGGER.info(f'Sending: {data}')
        for token, conn in self.players_connections.copy().items():
            conn.send(self.json_to_str(data))
