import re
from constants.server.network_keys import CheckRegex


def normalize_request(player_request):
    if '}{' in player_request and not re.search(CheckRegex.good_recv_re, player_request):
        player_request = f'{{{player_request.split("}{")[-1]}'

    return player_request
