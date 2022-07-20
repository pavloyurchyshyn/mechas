from constants.server.network_keys import ServerResponseCategories, PlayerActions, SRC
from game_logic.components.player_object import Player
from constants.server.game_logic_stages import GameLogicStagesConst


class ReadyStatusMixin:
    def __init__(self):
        self.ready_count = 0
        self.ready_locked = False

    def process_ready_status(self, token, data):
        if PlayerActions.READY_STATUS in data and self.stage != GameLogicStagesConst.Execution:
            player_update = self.data_to_send[SRC.PlayersUpdates].get(token, {})
            self.data_to_send[SRC.PlayersUpdates][token] = player_update
            player: Player = self.players_data[token]
            ready = data.pop(PlayerActions.READY_STATUS)
            if ready:
                if not player.ready:
                    self.ready_count += 1
                    player.ready = True
            else:
                if player.ready:
                    self.ready_count -= 1
                    player.ready = False

            player_update[ServerResponseCategories.ReadyState] = player.ready

            self.logger.info(f'{token} ready status: {player.ready}')

    def ready_all(self):
        self.__ready_status_to_all(True)

    def unready_all(self):
        self.__ready_status_to_all(False)

    def __ready_status_to_all(self, ready):
        self.logger.info(f'Set every player ready status: {ready}')

        self.ready_count = self.config.max_players_num if ready else 0
        player_updates = self.data_to_send[SRC.PlayersUpdates] = self.data_to_send.get(SRC.PlayersUpdates, {})

        for token, player in self.players_data.items():
            player.ready = ready
            player_updates[token] = player_update = player_updates.get(token, {})
            player_update[ServerResponseCategories.ReadyState] = player.ready
