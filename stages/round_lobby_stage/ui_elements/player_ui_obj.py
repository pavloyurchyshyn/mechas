from obj_properties.rect_form import Rectangle
from visual.UI_base.button_UI import Button
from visual.UI_base.text_UI import Text
from stages.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from pygame.draw import rect as draw_rect
from visual.sprites_functions import get_surface


class PlayerUIObj(Rectangle):
    def __init__(self, player_data, screen, **kwargs):
        super(PlayerUIObj, self).__init__(x=0,
                                          y=0,
                                          size_x=LobbyWindowsSizes.Players.PlayerUIObj.X_SIZE,
                                          size_y=LobbyWindowsSizes.Players.PlayerUIObj.Y_SIZE)
        self.screen = screen
        self.surface = get_surface(*self.sizes)
        self.players_data = player_data

        def print_():
            print('click kick', player_data)

        self.nickname = Text(f'PLayer {player_data["i"]}',
                             screen=self.surface,
                             size=(self.size_x*9/10, self.size_y)
                             )
        self.kick_button = Button(text='X',
                                  x=self.size_x - LobbyWindowsSizes.Players.PlayerUIObj.KickButton.X_SIZE,
                                  y=0,
                                  on_click_action=print_,
                                  background_color=(55, 0, 0),
                                  size_x=LobbyWindowsSizes.Players.PlayerUIObj.KickButton.X_SIZE,
                                  size_y=LobbyWindowsSizes.Players.PlayerUIObj.KickButton.Y_SIZE,
                                  screen=self.surface)
        self.kick_button.draw()

    def set_y(self, y):
        self.change_position_lt((self.x0, y))

    def click(self, xy):
        if self.collide_point(xy):
            xy = xy[0] - self.x0, xy[1] - self.y0
            for obj in (self.kick_button,):
                if obj.click(xy):
                    return True

    def update(self):
        self.kick_button.update()

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.kick_button.draw()
        self.nickname.draw()
        draw_rect(self.surface, (255, 255, 255), (0, 0, *self.sizes), 1)
        self.screen.blit(self.surface, self.left_top)
