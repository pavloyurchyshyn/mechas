from stages.round_lobby_stage.ui_elements.chat import ChatElement
from stages.round_lobby_stage.ui_elements.players_window import PlayersWindow
from visual.UI_base.button_UI import Button
from stages.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from common.global_mouse import GLOBAL_MOUSE
from common.global_keyboard import GLOBAL_KEYBOARD
from stages.round_lobby_stage.ui_elements.exit_pop_up import LobbyExitPopUp
from constants.network_keys import ServerResponseCategories, CheckRegex, SLC
from game_logic.components.player_object import Player
from common.logger import Logger

LOGGER = Logger().LOGGER


class LobbyWindow:
    def __init__(self, server_response, player, round_logic):  # server_response to process data TODO
        self.round_logic = round_logic
        self.this_player = player
        self.other_players = round_logic.other_players

        self.player_response = {}  # that a dict which sends to server
        self.chat_window = ChatElement(self.player_response)
        self.players_window = PlayersWindow(self.player_response, self.this_player)

        self.exit_pop_up = LobbyExitPopUp()
        self.go_button = Button(text='Go',
                                x=LobbyWindowsSizes.GoButton.X,
                                y=LobbyWindowsSizes.GoButton.Y,
                                size_x=LobbyWindowsSizes.GoButton.X_SIZE,
                                size_y=LobbyWindowsSizes.GoButton.Y_SIZE
                                )

        self.exit_button = Button(text='X',
                                  x=LobbyWindowsSizes.ExitButton.X,
                                  y=LobbyWindowsSizes.ExitButton.Y,
                                  size_x=LobbyWindowsSizes.ExitButton.X_SIZE,
                                  size_y=LobbyWindowsSizes.ExitButton.Y_SIZE,
                                  on_click_action=self.exit_pop_up.switch,
                                  )

    def update(self):
        self.chat_window.update()
        self.players_window.update()

        if self.exit_pop_up.active:
            self.exit_pop_up.update()

        clicked = False
        for b in (self.go_button, self.exit_button):
            b.update()
            if GLOBAL_MOUSE.lmb and not clicked and not self.exit_pop_up.active:
                clicked = b.click(GLOBAL_MOUSE.pos)

        if GLOBAL_KEYBOARD.ESC:
            self.exit_pop_up.switch()

    def draw(self):
        self.chat_window.draw()
        self.players_window.draw()
        self.go_button.draw()
        self.exit_button.draw()

        self.exit_pop_up.draw()

    def process_server_data(self, data):
        self.chat_window.add_messages(data.pop(ServerResponseCategories.MessagesToAll, []))
        self.__process_new_players(data)
        self.__process_kicks(data)

    def __process_kicks(self, data):
        if SLC.KickPlayer in data:
            LOGGER.info(f'Kicking {data[SLC.KickPlayer]}')
            token = data[SLC.KickPlayer]
            self.players_window.kick_player(token)

    def __process_new_players(self, data):
        if ServerResponseCategories.NewPlayers in data:
            LOGGER.info(f'Processing new players: {data[ServerResponseCategories.NewPlayers]}')
            for player_token, p_data in data[ServerResponseCategories.NewPlayers].items():
                if player_token not in self.round_logic.other_players and player_token != self.this_player.token:
                    obj = Player(**p_data)
                    self.round_logic.other_players[player_token] = obj
                    self.players_window.add_player(obj)
