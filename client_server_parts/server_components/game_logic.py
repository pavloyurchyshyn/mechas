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
        self.details_pool = DetailsPool(self.skills_pool, self.config.max_players_num)  # TODO

        pool_generator = PoolGenerator(self.config.max_players_num, self.config.details_pool_settings)
        self.details_pool.load_details_list(pool_generator.get_details_list())

    def run_game(self):
        LOGGER.info('Alive check started')
        LOGGER.info('Sever Game loop started.')
        update_delay = 1 / 32
        LOGGER.info(f'Tick rate {64}. Time per frame: {update_delay}')

        ROUND_CLOCK.set_time(-TIMEOUT)
        try:
            while self.server.alive:
                t = time()
                self.update()

                sl = update_delay - (time() - t)
                # LOGGER.info(f'Time spent for calculation {time() - t}, sleep {sl}')
                if sl > 0:
                    sleep(sl)

                ROUND_CLOCK.update(time() - t)

        except Exception as e:
            LOGGER.critical('Game loop stopped.')
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
        finally:
            self.server.alive = False
            self.alive = False
            LOGGER.info('Stopped')

    def start_player_handling(self, player_token):
        start_new_thread(self.player_thread, (self.server, player_token))

    def update(self):
        self.update_data_to_send()
        data = self.data_to_send.copy()
        self.data_to_send.clear()
        self.send_data(data)

    def update_data_to_send(self):
        self.data_to_send[ServerResponseCategories.MatchTime] = ROUND_CLOCK()

    def player_thread(self, server, player_token):
        try:
            connection = server.get_connection(player_token)

            while 1:
                player_request = connection.recv().decode()
                if player_request and player_request != '{}':
                    player_request = normalize_request(player_request)
                    player_request = self.str_to_json(player_request)
                    LOGGER.info(f'Received {player_token}: {player_request}')
                    self.process_data(player_token, player_request)

        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
            server.disconnect_player(player_token)

    def process_data(self, token, player_request: dict):
        self.data_to_send[SRC.PlayersUpdates] = self.data_to_send.get(SRC.PlayersUpdates, {})
        player_update = self.data_to_send[SRC.PlayersUpdates][token] = self.data_to_send[SRC.PlayersUpdates].get(token,
                                                                                                                 {})

        self.process_messages(token, player_request)
        self.process_ready_status(player_update, token, player_request)

    def process_ready_status(self, player_update, token, data):
        if PlayerActions.READY_STATUS in data:
            ready = data.pop(PlayerActions.READY_STATUS)
            player_update[ServerResponseCategories.ReadyState] = ready
            LOGGER.info(f'{token} ready status: {ready}')

    def send_data(self, data):
        if data.get('players_updates'):
            LOGGER.info(f'Sending: {data}')
        for token, conn in self.players_connections.copy().items():
            conn.send(self.json_to_str(data))
