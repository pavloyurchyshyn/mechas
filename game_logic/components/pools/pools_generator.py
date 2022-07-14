from settings.mechas.default_details_pool import DEFAULT_DETAILS_POOL_SETTINGS, DEFAULT_START_DETAILS
from common.logger import Logger
from constants.mechas.detail_const import MechSerializeConst


class PoolGenerator:
    def __init__(self, players_num: int,
                 detail_pool_settings: dict = DEFAULT_DETAILS_POOL_SETTINGS,
                 ):
        self.players_num = players_num
        self.detail_pool_settings = detail_pool_settings
        self.default_details = dict.fromkeys(range(players_num))

    def get_default_details(self, default_set):
        # TODO not ready
        return {
            MechSerializeConst.Body: []

        }

    def get_details_list(self):
        l = []
        Logger().info(f'Generating {self.detail_pool_settings}')
        for detail_name, count in self.detail_pool_settings.items():
            Logger().info(f'Detail {detail_name} {count * self.players_num // 1}')
            for i in range(count * self.players_num // 1):
                l.append((detail_name, None))

        return l
