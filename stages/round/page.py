from stages.round.UI import RoundUI
from stages.round.windows.world_window.window import ArenaWindow
from stages.round.windows.top_bar import TopBar
from stages.round.windows.exit_pop_up import ExitPopUp
from stages.round.windows.cards_windows.cards_window import CardsWindow
from stages.round.windows.mech_window.mech_window import MechWindow
from stages.round.windows.chat import ChatWindow
from stages.round.windows.ready import ReadyWindow
from constants.network_keys import ServerResponseCategories


class Round:
    def __init__(self):
        self.player_response = {}

        self.player = None
        self.other_players = {}
        self.arena_window = ArenaWindow()
        self.top_bar = TopBar()
        self.exit_pop_up = ExitPopUp()
        self.cards_window = CardsWindow()
        self.mech_window = MechWindow()
        self.chat_window = ChatWindow(self.player_response)

        self.round_ui = RoundUI()

        self.ready = ReadyWindow(self.player_response)

    def update(self):
        if self.exit_pop_up.active:
            self.exit_pop_up.update()
        else:
            self.arena_window.update()
            self.top_bar.update()

        self.chat_window.update()
        self.ready.update()

    def process_server_data(self, data: dict):
        self.chat_window.add_messages(data.pop(ServerResponseCategories.MessagesToAll, {}))
        this_player_data = data.pop(ServerResponseCategories.PlayersUpdates, {}).pop(self.player.token, {})
        self.ready.process_server_data(this_player_data)

    def draw(self):
        self.arena_window.draw()

        # self.round_ui.draw()

        self.top_bar.draw()

        if self.exit_pop_up.active:
            self.exit_pop_up.draw()

        self.cards_window.draw()
        self.mech_window.draw()
        self.chat_window.draw()

        self.ready.draw()

    def set_player(self, player):
        self.player = player

    def add_other_player(self, token, player):
        self.other_players[token] = player

    def replace_other_player(self, old_token, new_token):
        self.other_players[new_token] = self.other_players.pop(old_token)
