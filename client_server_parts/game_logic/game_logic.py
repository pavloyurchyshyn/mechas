from constants.server.network_keys import ServerResponseCategories, SRC
from constants.server.game_logic_stages import GameLogicStagesConst
from common.logger import Logger
from common.global_clock import ROUND_CLOCK
from game_logic.components.pools.skills_pool import SkillsPool
from game_logic.components.pools.details_pool import DetailsPool
from game_logic.components.pools.pools_generator import PoolGenerator
from client_server_parts.server_components.config import ServerConfig

from client_server_parts.server_components.mixins.message_processor import MessageProcessorMixin
from client_server_parts.game_logic.mixins.ready_status_mixin import ReadyStatusMixin
from client_server_parts.game_logic.mixins.mech_logic_mixin import MechLogicMixin
from mechas.mech_serializer import MechSerializer

from constants.server.network_end_symbols import END_OF_REQUEST

TIMEOUT = 45


class GameLogic(MessageProcessorMixin,
                ReadyStatusMixin,
                MechLogicMixin,
                ):
    logger = Logger('server_logs', 0, std_handler=0).LOGGER

    def __init__(self, server):
        self.init()

        self.mech_serializer = None

        self.server = server
        self.config: ServerConfig = self.server.config

        self.players_connections: dict = server.players_connections
        self.players_data: dict = server.players_data

        self.json_to_str = server.json_to_str
        self.str_to_json = server.str_to_json
        self.alive = True

        self.data_to_send = server.data_to_send

        self.skills_pool: SkillsPool = None
        self.details_pool: DetailsPool = None

        self.stage = GameLogicStagesConst.Preparing
        self.players_default_details = {}

    def init(self):
        for class_ in self.__class__.__mro__:
            if class_ != GameLogic:
                class_.__init__(self)

    def build_round(self):
        self.skills_pool = SkillsPool()
        self.details_pool = DetailsPool(self.skills_pool)  # TODO
        self.mech_serializer = MechSerializer(self.details_pool)

        pool_generator = PoolGenerator(self.config.max_players_num, self.config.details_pool_settings)
        self.details_pool.load_details_list(pool_generator.get_details_list())
        self.players_default_details = self.details_pool.get_default_details(self.config.default_details_settings,
                                                                             self.config.max_players_num)
        self.build_players_mechas()
        self.update_players_inventory_size()

    def update_players_inventory_size(self):
        for player in self.players_data.values():
            player.inventory.update_size(self.config.inventory_size)

    def update(self):
        self.update_data_to_send()
        self.check_for_timeout()
        data = self.data_to_send.copy()
        self.data_to_send.clear()
        self.send_data(data)

    def check_for_timeout(self):
        if ROUND_CLOCK.time > 0:
            self.send_bare_message('Round timer end')
            ROUND_CLOCK.set_time(self.config.planing_time)
            self.unready_all()

    def update_data_to_send(self):
        self.data_to_send[ServerResponseCategories.MatchTime] = ROUND_CLOCK()
        self.data_to_send[ServerResponseCategories.ReadyCount] = self.ready_count

    def process_received(self, token, player_request: dict):
        self.data_to_send[SRC.PlayersUpdates] = self.data_to_send.get(SRC.PlayersUpdates, {})
        self.process_messages(token, player_request)
        self.process_ready_status(token, player_request)

    def send_data(self, data):
        # if data.get('players_updates'):
        self.logger.info(f'Sending: {data}')
        data = self.json_to_str(data) + END_OF_REQUEST
        for token, conn in self.players_connections.copy().items():
            conn.send(data)
