from visual.UI_base.text_UI import Text
from constants.server.network_keys import NetworkKeys, SLC
from stages.play_stage.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from visual.UI_base.button_UI import Button
from common.global_mouse import GLOBAL_MOUSE


class PlayersNumber:
    def __init__(self, server_response, player_response):
        self.player_response = player_response
        self.players_number_txt = Text(server_response[NetworkKeys.PlayersNumber],
                                       size=(LobbyWindowsSizes.PlayersNumber.NumberText.X_SIZE,
                                             LobbyWindowsSizes.PlayersNumber.NumberText.Y_SIZE),
                                       x=LobbyWindowsSizes.PlayersNumber.NumberText.X,
                                       y=LobbyWindowsSizes.PlayersNumber.NumberText.Y,
                                       auto_draw=False,
                                       )
        self.add_button = Button(size_x=LobbyWindowsSizes.PlayersNumber.AddButton.X_SIZE,
                                 size_y=LobbyWindowsSizes.PlayersNumber.AddButton.Y_SIZE,
                                 x=LobbyWindowsSizes.PlayersNumber.AddButton.X,
                                 y=LobbyWindowsSizes.PlayersNumber.AddButton.Y,
                                 text='+',
                                 on_click_action=self.add_player,
                                 )

        self.minus_button = Button(size_x=LobbyWindowsSizes.PlayersNumber.MinusButton.X_SIZE,
                                   size_y=LobbyWindowsSizes.PlayersNumber.MinusButton.Y_SIZE,
                                   x=LobbyWindowsSizes.PlayersNumber.MinusButton.X,
                                   y=LobbyWindowsSizes.PlayersNumber.MinusButton.Y,
                                   text='-',
                                   on_click_action=self.minus_player,
                                   )

    def process_server_data(self, data):
        if SLC.PlayersNumber in data:
            self.players_number_txt.change_text(data[SLC.PlayersNumber])

    def add_player(self):
        self.player_response[SLC.AddPlayersNumber] = True

    def minus_player(self):
        self.player_response[SLC.MinusPlayersNumber] = True

    def update(self):
        clicked = False
        for obj in (self.minus_button, self.add_button):
            obj.update()
            if GLOBAL_MOUSE.lmb and not clicked:
                clicked = obj.click(GLOBAL_MOUSE.pos)

    def draw(self):
        self.players_number_txt.draw()
        self.add_button.draw()
        self.minus_button.draw()
