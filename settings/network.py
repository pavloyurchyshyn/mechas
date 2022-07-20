from common.save_and_load_json_config import get_from_common_config
import socket
from constants.server.network_keys import NetworkKeys, PlayerAttrs

DEFAULT_PORT = 8002
RECV_SIZE = 2048
GAME_TICK_RATE = 64

DEFAULT_TIME_PER_ROUND = 60
END_ROUND_TIME = -5  # seconds
TIME_TO_START_ROUND = -10
WAIT_FOR_PLAYERS_TIME = -60

CONNECTION_TIMEOUT = 10

SERVER_FILE_NAME = 'server.exe'
SERVER_PYTHON_FILE_NAME = 'server.py'

NETWORK_DATA = {
    NetworkKeys.Address: socket.gethostbyname(socket.gethostname()),
    NetworkKeys.Port: DEFAULT_PORT,
    PlayerAttrs.Nickname: get_from_common_config(PlayerAttrs.Nickname, 'NoNickname'),
    NetworkKeys.Password: '.',
    NetworkKeys.PlayerNumber: 2,
}


def update_host_address(text):
    text = text.split(':')
    NETWORK_DATA[NetworkKeys.Address] = text[0]
    NETWORK_DATA[NetworkKeys.Port] = text[1]


def anon_host(host):
    if type(host) is tuple:
        host = f"{host[0]}:{host[1]}"
    host = host.strip()
    host = host.split(':')[0]
    pre, post = host[:2], host[-2:]
    host = host[2:-2]

    for i in range(0, 10):
        host = host.replace(str(i), '*')

    host = f'{pre}{host}{post}'
    return f'{host}'


SERVER_ARGUMENTS = {
    f'--{NetworkKeys.Port}': [DEFAULT_PORT, 'Server Port'],
    f'--{NetworkKeys.PlayerNumber}': [2, 'Number of players'],
    f'--{NetworkKeys.Password}': ['.', 'Lobby password'],
    f'--{NetworkKeys.TeamNames}': ['red,blue', 'Coma separated teams names'],
    f'--{NetworkKeys.AdminToken}': ['None', 'Admin access key'],
}
