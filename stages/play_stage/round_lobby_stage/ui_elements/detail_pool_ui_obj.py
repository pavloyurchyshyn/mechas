from visual.UI_base.text_UI import Text
from obj_properties.rect_form import Rectangle
from stages.play_stage.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from visual.sprites_functions import get_surface


class DetailUIElement(Rectangle):
    def __init__(self, screen, name):
        super(DetailUIElement, self).__init__(x=0, y=0,
                                              size_x=LobbyWindowsSizes.DetailsPoolSettings.DetailUIObj.X_SIZE,
                                              size_y=LobbyWindowsSizes.DetailsPoolSettings.DetailUIObj.Y_SIZE,
                                              )

        self.name = name
        self.screen = screen
        self.surface = None
        self.name_text = None

        self.build()

    def build(self):
        self.surface = get_surface(*self.sizes)
        self.name_text = Text(text=f"{self.name}",
                              screen=self.surface,
                              size=(self.size_x / 10, self.size_y),
                              x=2,
                              )

    def draw(self):
        self.screen.blit(self.surface, self.left_top)
