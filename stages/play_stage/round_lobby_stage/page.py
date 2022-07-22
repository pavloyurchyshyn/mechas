from stages.play_stage.round_lobby_stage.ui_elements.chat import ChatElement
from stages.play_stage.round_lobby_stage.ui_elements.players_window import PlayersWindow
from stages.play_stage.round_lobby_stage.ui_elements.exit_pop_up import LobbyExitPopUp
from stages.play_stage.round_lobby_stage.ui_elements.details_pool_settings import DetailPoolSettings
from stages.play_stage.round_lobby_stage.ui_elements.players_number import PlayersNumber

from stages.play_stage.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes

from visual.UI_base.button_UI import Button

from common.global_mouse import GLOBAL_MOUSE
from common.global_keyboard import GLOBAL_KEYBOARD
from common.logger import Logger

from constants.server.network_keys import ServerResponseCategories, SLC, NetworkKeys

from game_logic.components.player_object import Player

LOGGER = Logger().LOGGER


class LobbyWindow:
    def __init__(self, server_response, player, round_logic):  # server_response to process data TODO
        self.round_logic = round_logic
        self.this_player = player
        self.other_players = round_logic.other_players

        self.player_response = {}  # that a dict which sends to server
        self.chat_window = ChatElement(self.player_response)
        self.players_window = PlayersWindow(self.player_response, self.this_player)
        self.players_number = PlayersNumber(server_response, self.player_response)
        self.exit_pop_up = LobbyExitPopUp()
        self.go_button = Button(text='Go',
                                x=LobbyWindowsSizes.GoButton.X,
                                y=LobbyWindowsSizes.GoButton.Y,
                                active=self.this_player.is_admin,
                                size_x=LobbyWindowsSizes.GoButton.X_SIZE,
                                size_y=LobbyWindowsSizes.GoButton.Y_SIZE,
                                on_click_action=self.start_game,
                                non_active_after_click=False,
                                )

        self.exit_button = Button(text='X',
                                  x=LobbyWindowsSizes.ExitButton.X,
                                  y=LobbyWindowsSizes.ExitButton.Y,
                                  size_x=LobbyWindowsSizes.ExitButton.X_SIZE,
                                  size_y=LobbyWindowsSizes.ExitButton.Y_SIZE,
                                  on_click_action=self.exit_pop_up.switch,
                                  non_active_after_click=False,
                                  )

        self.details_pool_settings = DetailPoolSettings(pool_setting=self.round_logic.details_pool_settings,
                                                        details_pool=self.round_logic.details_pool)

    def start_game(self):
        LOGGER.info(f'Send start game request')
        self.player_response[SLC.StartGame] = True

    def update(self):
        self.chat_window.update()
        self.players_window.update()
        self.details_pool_settings.update()
        self.players_number.update()

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
        self.details_pool_settings.draw()
        self.exit_pop_up.draw()
        self.players_number.draw()

    def process_server_data(self, data):
        self.chat_window.add_messages(data.pop(ServerResponseCategories.MessagesToAll, []))
        self.__process_new_players(data)
        self.__process_kicks(data)
        self.players_number.process_server_data(data)

    def __process_kicks(self, data):
        if SLC.KickPlayer in data:
            LOGGER.info(f'Kicking {data[SLC.KickPlayer]}')
            token = data[SLC.KickPlayer]
            self.other_players.pop(token)
            self.players_window.kick_player(token)

    def __process_new_players(self, data):
        if ServerResponseCategories.NewPlayers in data:
            LOGGER.info(f'Processing new players: {data[ServerResponseCategories.NewPlayers]}')
            for player_token, p_data in data[ServerResponseCategories.NewPlayers].items():
                if player_token not in self.round_logic.other_players and player_token != self.this_player.token:
                    obj = Player(**p_data)
                    self.round_logic.other_players[player_token] = obj
                    self.players_window.add_player(obj)
