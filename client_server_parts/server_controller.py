import subprocess
import os
from settings.base import ROOT_OF_GAME
from settings.network import *
from constants.server.network_keys import NetworkKeys, PlayerAttrs
import time
from common.save_and_load_json_config import get_from_common_config
from _thread import start_new_thread
from common.logger import Logger

LOGGER = Logger()


class ServerController:
    def __init__(self):
        self._ip_address = socket.gethostbyname(socket.gethostname())
        self.port = DEFAULT_PORT
        self._server_process = None

        self.players_number = 2
        self.password = ''

    def run_server(self):
        self.update_parameters()
        arguments = self.get_arguments()
        if os.path.exists(os.path.join(ROOT_OF_GAME, SERVER_FILE_NAME)):
            arguments = [os.path.join(ROOT_OF_GAME, SERVER_FILE_NAME), *arguments]
        else:
            arguments = ['python', os.path.join(ROOT_OF_GAME, SERVER_PYTHON_FILE_NAME), *arguments]
        LOGGER.info('Server started.')
        LOGGER.info(f'Arguments.{arguments}')
        self._server_process = subprocess.Popen(arguments)

    def stop_server(self):
        start_new_thread(self.__terminate, ())

    def __terminate(self):
        LOGGER.info(f'Terminating server')
        if self._server_process:
            time.sleep(5)
            self._server_process.terminate()
            LOGGER.info(f'Successfully terminated server')
        self._server_process = None

    def get_arguments(self) -> list:
        arguments = [f'--{NetworkKeys.Port}', str(NETWORK_DATA[NetworkKeys.Port]),
                     f'--{NetworkKeys.PlayerNumber}', str(NETWORK_DATA[NetworkKeys.PlayerNumber]),
                     f'--{NetworkKeys.Password}', str(NETWORK_DATA[NetworkKeys.Password]),
                     f'--{NetworkKeys.AdminToken}', str(get_from_common_config(PlayerAttrs.Token, def_value='None')),
                     ]

        for key, values in SERVER_ARGUMENTS.items():
            if key not in arguments:
                arguments.append(key)
                arguments.append(str(values[0]))

        return arguments

    def update_parameters(self):
        self.players_number = NETWORK_DATA[NetworkKeys.PlayerNumber]
        self.password = NETWORK_DATA[NetworkKeys.Password]
        self.port = NETWORK_DATA[NetworkKeys.Port]

    def __del__(self):
        self.stop_server()
