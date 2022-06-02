import traceback
from _thread import start_new_thread
from time import sleep, time
from constants.network_keys import ServerResponseCategories, PlayerActions
from common.logger import Logger
from common.global_clock import GLOBAL_CLOCK

LOGGER = Logger('server_logs', 0, std_handler=0).LOGGER


class GameLogic:
    def __init__(self, server):
        self.server = server
        self.players_connections = server.players_connections
        self.json_to_str = server.json_to_str
        self.str_to_json = server.str_to_json
        self.alive = True

        self.data_to_send = {}

    def run_game(self):
        LOGGER.info('Alive check started')
        LOGGER.info('Sever Game loop started.')
        update_delay = 1 / 32
        LOGGER.info(f'Tick rate {64}. Time per frame: {update_delay}')

        finish = time() + 60
        try:
            while self.server.alive:
                t = time()
                self.update()

                if time() > finish:
                    self.server.alive = False
                    LOGGER.info(f'Timeout')

                GLOBAL_CLOCK.update(time() - t)

                sl = update_delay - (time() - t)
                # LOGGER.info(f'Time spent for calculation {time() - t}, sleep {sl}')
                if sl > 0:
                    sleep(sl)
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

    def player_thread(self, server, player_token):
        try:
            connection = server.get_connection(player_token)
            server_response = self.data_to_send

            while 1:
                player_data = connection.recv().decode()
                if '}{' in player_data:
                    player_data = f'{{{player_data.split("}{")[-1]}'

                player_data = self.str_to_json(player_data)
                LOGGER.info(f'Received {player_token}: {player_data}')
                self.process_data(player_token, player_data)

        except Exception as e:
            LOGGER.error(e)
            server.disconnect_player(player_token)

    def update(self):
        self.update_data_to_send()
        data = self.data_to_send.copy()
        self.data_to_send.clear()
        self.send_data(data)

    def update_data_to_send(self):
        self.data_to_send[ServerResponseCategories.MatchTime] = 1

    def process_data(self, token, data: dict):
        self.process_messages(token, data)

    def process_messages(self, token, data):
        if PlayerActions.MESSAGE in data:
            message = data.pop(PlayerActions.MESSAGE)
            if message:
                name = self.server.players_names.get(token)
                message = f'{name}: {message}'
                messages = self.data_to_send.get(ServerResponseCategories.MessagesToAll, [])
                messages.append(message)
                self.data_to_send[ServerResponseCategories.MessagesToAll] = messages

    def send_data(self, data):
        if len(data) > 1:
            LOGGER.info(f'Sending: {data}')
        for token, conn in self.players_connections.copy().items():
            conn.send(self.json_to_str(data))
