from socket import socket
from settings.network import CONNECTION_TIMEOUT
from time import time
from common.logger import Logger


class ConnectionHandler:

    def __init__(self, connection: socket, player_id=None):
        self.connection: socket = connection
        self._last_successful_send = time()
        self.player_id = player_id
        self.alive = 1

    def change_connection(self, connection):
        self.connection = connection

    def send(self, data):
        try:
            self.connection.send(data)
        except Exception as e:
            self.check_for_timeout()
        else:
            self._last_successful_send = time()

    def recv(self, size=2048):
        try:
            data = self.connection.recv(size)
            self._last_successful_send = time()
            return data

        except Exception as e:
            self.check_for_timeout()
            return b''

    def check_for_timeout(self):
        if CONNECTION_TIMEOUT < time() - self._last_successful_send:
            self.alive = 0
            raise TimeoutError('Connection lost')

    def close(self):
        try:
            self.connection.close()
        except Exception as e:
            Logger().LOGGER.error(f'Failed to disconnect {self.player_id}: {e}')
        else:
            Logger().LOGGER.info(f'{self.player_id} disconnected!')

    def __del__(self):
        try:
            self.close()
        except:
            pass
