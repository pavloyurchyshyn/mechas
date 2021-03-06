import socket
import json
import traceback

from constants.server.network_keys import NetworkKeys, ServerConnectAnswers, PlayerAttrs
from common.save_and_load_json_config import save_to_common_config, get_from_common_config
from common.logger import Logger
from settings.network import DEFAULT_PORT, NETWORK_DATA, RECV_SIZE
from constants.server.network_end_symbols import END_OF_REQUEST

LOGGER = Logger()


class Network:
    def __init__(self):
        self.connection = None
        self.server = ""
        self.port = DEFAULT_PORT
        self.server_addr = (self.server, self.port)
        self.password = ''
        self.nickname = ''
        self.connected = False
        self.credentials = {}

        self.token = get_from_common_config(PlayerAttrs.Token, def_value=None)

    def update_network_data(self):
        self.server = NETWORK_DATA[NetworkKeys.Address]
        self.port = NETWORK_DATA[NetworkKeys.Port]
        self.nickname = NETWORK_DATA[PlayerAttrs.Nickname]
        self.password = NETWORK_DATA[NetworkKeys.Password]
        self.server_addr = (self.server, self.port)

        self.credentials.clear()
        self.credentials[PlayerAttrs.Nickname] = self.nickname
        self.credentials[NetworkKeys.Password] = self.password
        self.credentials[PlayerAttrs.Token] = get_from_common_config(PlayerAttrs.Token, def_value=self.token)

    def connect(self):
        if self.connection:
            self.connection.close()

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.update_network_data()

        try:
            self.connection.connect(self.server_addr)
            self.connection.send(self.json_to_str(self.credentials))
            LOGGER.info(f"Connection server request {self.credentials}")
            recv = b''
            while True:
                recv_ = self.connection.recv(4096)
                if recv_.endswith(END_OF_REQUEST):
                    recv += recv_
                    break
                recv += recv_

            response = self.str_to_json(recv.replace(END_OF_REQUEST, b'').decode())
            LOGGER.info(f"Connection server response {response}")
            conn_sts = response.get(ServerConnectAnswers.CONNECTION_ANSWER)
            LOGGER.info(f'Connection status: {conn_sts}')
            if conn_sts == ServerConnectAnswers.Connected:
                self.connected = True
                self.token = response.get(PlayerAttrs.Token)
                save_to_common_config(key=PlayerAttrs.Token, value=self.token)

                return response
            else:
                LOGGER.warn(f'Bad connection answer: {response.get(ServerConnectAnswers.CONNECTION_ANSWER)}')
                self.disconnect()
                return response

        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
            self.disconnect()
            return {ServerConnectAnswers.CONNECTION_ANSWER: ServerConnectAnswers.FailedToConnect,
                    NetworkKeys.ServerMessages: f'{e}'}

    def disconnect(self):
        try:
            self.connection.close()
        except Exception as e:
            LOGGER.error(e)
        finally:
            self.connected = False

    @staticmethod
    def str_to_json(string):
        try:
            if string:
                return json.loads(string)
            else:
                return {}
        except Exception as e:
            LOGGER.error(f'Failed to convert {string} to json: {e}')
            # LOGGER.error(traceback.format_exc())
            return {}

    @staticmethod
    def json_to_str(json_):
        return json.dumps(json_).encode()

    def send(self, data):
        try:
            if data:
                LOGGER.info(f'Sending: {data}')
            self.connection.send(self.json_to_str(data))
        except socket.error as e:
            LOGGER.error(f"Failed to send data {e}")
            self.disconnect()

    def bulk_receive(self):
        recv = b''
        while True:
            recv_ = self.connection.recv(4096)
            if recv_.endswith(END_OF_REQUEST):
                recv += recv_
                break
            recv += recv_

        return (r.decode() for r in recv.split(END_OF_REQUEST)[:-1])

    def receive(self):
        recv = b''
        while True:
            recv_ = self.connection.recv(4096)
            if recv_.endswith(END_OF_REQUEST):
                recv += recv_
                break
            recv += recv_

        return recv.replace(END_OF_REQUEST, b'').decode()
#        return self.connection.recv(RECV_SIZE).replace(b'\x00\x00', b'').decode()

    def get_data(self):
        data = self.receive()
        return self.str_to_json(data)

    def update(self, data):
        self.send(data)

        return self.get_data()

    def __del__(self):
        self.disconnect()
