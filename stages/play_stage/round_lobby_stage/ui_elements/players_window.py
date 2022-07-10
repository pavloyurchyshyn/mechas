from obj_properties.rect_form import Rectangle
from stages.play_stage.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from visual.main_window import MAIN_SCREEN
from stages.play_stage.round_lobby_stage.ui_elements.players_container import PlayersContainer
from visual.UI_base.text_UI import Text


class PlayersWindow(Rectangle):
    def __init__(self, player_request, this_player):
        self.this_player = this_player
        self.player_request = player_request
        super(PlayersWindow, self).__init__(x=LobbyWindowsSizes.Players.X,
                                            y=LobbyWindowsSizes.Players.Y,
                                            size_x=LobbyWindowsSizes.Players.X_SIZE,
                                            size_y=LobbyWindowsSizes.Players.Y_SIZE)

        self.players_header = Text('#\t\tNickname\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t Kick', x=self.x0,
                                   y=self.y0 - 20)

        self.players_container = PlayersContainer(x=LobbyWindowsSizes.Players.X,
                                                  y=LobbyWindowsSizes.Players.Y,
                                                  size_x=LobbyWindowsSizes.Players.X_SIZE,
                                                  size_y=LobbyWindowsSizes.Players.Y_SIZE,
                                                  screen=MAIN_SCREEN,
                                                  player_window=self)

    def add_player(self, player_obj):
        self.players_container.add_player(player_obj)

    def kick_player(self, token: str):
        self.players_container.kick_player(token)

    def update(self):
        self.players_container.update()

    def draw(self):
        # draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
        self.players_container.draw()
        self.players_header.draw()
