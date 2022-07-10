from obj_properties.rect_form import Rectangle
from visual.UI_base.button_UI import Button
from visual.UI_base.text_UI import Text
from stages.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from pygame.draw import rect as draw_rect
from visual.sprites_functions import get_surface
from settings.global_parameters import test_draw_status_is_on
from pygame.draw import circle as draw_circle
from visual.main_window import MAIN_SCREEN
from stages.round_lobby_stage.settings.player_container import Colors
from game_logic.components.player_object import Player
from constants.network_keys import SLC



class PlayerUIObj(Rectangle):
    def __init__(self, this_player, player_obj: Player, screen, request_dict: dict, **kwargs):
        super(PlayerUIObj, self).__init__(x=0,
                                          y=0,
                                          size_x=LobbyWindowsSizes.Players.PlayerUIObj.X_SIZE,
                                          size_y=LobbyWindowsSizes.Players.PlayerUIObj.Y_SIZE,
                                          )
        self.request_dict = request_dict
        self.this_client_player: Player = this_player

        self.player: Player = player_obj

        self.screen = screen
        self.surface = None

        self.number_text = None
        self.nickname_text = None
        self.kick_button = None
        self.build()

        self.under_mouse = False

    def __on_click_function(self):
        self.request_dict[SLC.KickPlayer] = self.player.token

    def build(self):
        self.surface = get_surface(*self.sizes)
        self.surface.fill(Colors.back_color_this if self.this_client_player == self.player else Colors.back_color)

        self.number_text = Text(text=f"#{self.player.number}",
                                screen=self.surface,
                                size=(self.size_x / 10, self.size_y),
                                x=2,
                                )
        self.nickname_text = Text(f'{"[A] " if self.player.is_admin else ""}Player {self.player.nickname}',
                                  screen=self.surface,
                                  size=(self.size_x * 9 / 10, self.size_y),
                                  x=self.size_x // 10,
                                  )

        can_kick = self.this_client_player != self.player and self.this_client_player.is_admin and not self.player.is_admin
        self.kick_button = Button(text='X',
                                  x=self.size_x - LobbyWindowsSizes.Players.PlayerUIObj.KickButton.X_SIZE,
                                  y=0,
                                  text_color=Colors.X_text_color,
                                  active=can_kick,
                                  visible=can_kick,
                                  on_click_action=self.__on_click_function,
                                  border_color=Colors.X_button_bord_color,
                                  background_color=Colors.X_button_back_color,
                                  size_x=LobbyWindowsSizes.Players.PlayerUIObj.KickButton.X_SIZE,
                                  size_y=LobbyWindowsSizes.Players.PlayerUIObj.KickButton.Y_SIZE,
                                  screen=self.surface)
        self.kick_button.draw()

    def reload_player_number(self):
        self.number_text.change_text(f"#{self.player.number}")

    def set_y(self, y):
        self.change_position_lt((self.x0, y))

    def click(self, xy):
        if self.collide_point(xy):
            xy = xy[0] - self.x0, xy[1] - self.y0
            for obj in (self.kick_button,):
                if obj.click(xy):
                    return True

    def update(self, m_pos):
        self.kick_button.update()

        self.under_mouse = False
        if self.collide_point(m_pos):
            self.under_mouse = True

    def draw(self):
        self.surface.fill(Colors.back_color_mouse) if self.under_mouse else self.surface.fill(Colors.back_color)
        self.nickname_text.draw()
        self.number_text.draw()
        draw_rect(self.surface, Colors.border_color, (0, 0, *self.sizes), 1)
        self.kick_button.draw()
        self.screen.blit(self.surface, self.left_top)
