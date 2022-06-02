from stages.round.UI import RoundUI
from stages.round.windows.world_window.window import ArenaWindow
from stages.round.windows.top_bar import TopBar
from stages.round.windows.exit_pop_up import ExitPopUp
from stages.round.windows.cards_windows.cards_window import CardsWindow
# from stages.round.windows.mech_window import MechWindow
from stages.round.windows.chat import ChatWindow
from constants.network_keys import ServerResponseCategories


class Round:
    def __init__(self):
        self.player_response = {}
        self.arena_window = ArenaWindow()
        self.top_bar = TopBar()
        self.exit_pop_up = ExitPopUp()
        self.cards_window = CardsWindow()
        # self.mech_window = MechWindow()
        self.chat_window = ChatWindow(self.player_response)

        self.round_ui = RoundUI()

    def update(self):
        if self.exit_pop_up.active:
            self.exit_pop_up.update()
        else:
            # self.round_ui.update()
            self.arena_window.update()
            self.top_bar.update()

        self.chat_window.update()

    def update_chat(self,player_response):
        self.chat_window.update(player_response)

    def draw(self):
        self.arena_window.draw()

        # self.round_ui.draw()

        self.top_bar.draw()

        if self.exit_pop_up.active:
            self.exit_pop_up.draw()

        self.cards_window.draw()
        # self.mech_window.draw()
        self.chat_window.draw()

