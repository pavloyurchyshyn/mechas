import random
from argparse import ArgumentParser
from settings.network import SERVER_ARGUMENTS
from common.logger import Logger
from settings.mechas.default_details_pool import DEFAULT_DETAILS_POOL_SETTINGS
LOGGER = Logger('server_logs', 0, std_handler=0)


class ServerConfig:
    def __init__(self):
        arg_parser = ArgumentParser()

        for argument, value in SERVER_ARGUMENTS.items():
            arg_parser.add_argument(argument, default=value[0], help=value[1])

        arguments = arg_parser.parse_args()
        LOGGER.info(f'Start args {arguments.__dict__}')

        self.max_players_num = 2
        self.game_password = arguments.password
        self.server_port = int(arguments.port)
        self.main_admin_key = str(arguments.admin_token) if arguments.admin_token != 'None' else '_'
        self.admins_list = set(filter(bool, self.main_admin_key.split(',')))

        self.details_pool_settings = DEFAULT_DETAILS_POOL_SETTINGS.copy()
        self.admins_list.add(self.main_admin_key)
        self.seed = random.getrandbits(32)

        self.host_token = self.main_admin_key