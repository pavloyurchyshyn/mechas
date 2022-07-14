from visual.UI_base.text_UI import Text
from visual.UI_base.input_element_UI import InputElement
from obj_properties.rect_form import Rectangle
from stages.play_stage.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from visual.sprites_functions import get_surface
from stages.play_stage.round_lobby_stage.settings.player_container import Colors
from pygame.draw import rect as draw_rect


class DetailUIElement(Rectangle):
    def __init__(self, screen, detail_class, pool_settings):
        super(DetailUIElement, self).__init__(x=0, y=0,
                                              size_x=LobbyWindowsSizes.DetailsPoolSettings.DetailUIObj.X_SIZE,
                                              size_y=LobbyWindowsSizes.DetailsPoolSettings.DetailUIObj.Y_SIZE,
                                              )
        self.pool_settings: dict = pool_settings
        self.detail_class = detail_class

        self.details_per_player: InputElement = None
        self.screen = screen
        self.surface = None
        self.name_text: Text = None
        self.under_mouse = False
        self.build()

    def update(self, m_pos):
        self.surface.fill(Colors.back_color_mouse) if self.under_mouse else self.surface.fill(Colors.back_color)
        self.under_mouse = False
        if self.collide_point(m_pos):
            self.under_mouse = True

        for obj in (self.details_per_player, ):
            obj.update()

    def click(self, xy):
        if self.collide_point(xy):
            xy = xy[0] - self.x0, xy[1] - self.y0
            for obj in (self.details_per_player,):
                if obj.click(xy):
                    return True

    def build(self):
        self.surface = get_surface(*self.sizes)
        self.name_text = Text(text=f"{self.detail_class.verbal_name}",
                              screen=self.surface,
                              size=(self.size_x / 10, self.size_y),
                              x=2,
                              )

        self.details_per_player = InputElement(x=2 + self.size_x / 2,
                                               y=0,
                                               size_x=self.size_x // 10,
                                               size_y=self.size_y,
                                               text=self.pool_settings[self.detail_class.name],
                                               screen=self.surface,
                                               )

    def draw(self):
        self.surface.fill(Colors.back_color_mouse) if self.under_mouse else self.surface.fill(Colors.back_color)
        self.name_text.draw()
        self.details_per_player.draw()
        draw_rect(self.surface, Colors.border_color, (0, 0, *self.sizes), 1)

        self.screen.blit(self.surface, self.left_top)
