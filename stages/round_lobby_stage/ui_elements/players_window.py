from obj_properties.rect_form import Rectangle
from stages.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from visual.main_window import MAIN_SCREEN
from stages.round_lobby_stage.ui_elements.players_container import PlayersContainer
from visual.UI_base.text_UI import Text


class PlayersWindow(Rectangle):
    def __init__(self):
        super(PlayersWindow, self).__init__(x=LobbyWindowsSizes.Players.X,
                                            y=LobbyWindowsSizes.Players.Y,
                                            size_x=LobbyWindowsSizes.Players.X_SIZE,
                                            size_y=LobbyWindowsSizes.Players.Y_SIZE)

        self.players_header = Text('Players', x=self.x0, y=self.y0 - 20)

        self.players_container = PlayersContainer(x=LobbyWindowsSizes.Players.X,
                                                  y=LobbyWindowsSizes.Players.Y,
                                                  size_x=LobbyWindowsSizes.Players.X_SIZE,
                                                  size_y=LobbyWindowsSizes.Players.Y_SIZE,
                                                  screen=MAIN_SCREEN)

        for i in range(16):
            self.players_container.add_player({'i': i})



    def update(self):
        self.players_container.update()


    def draw(self):
        # draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
        self.players_container.draw()
        self.players_header.draw()
