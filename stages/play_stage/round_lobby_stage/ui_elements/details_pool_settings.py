from visual.UI_base.obj_scroll_container_UI import ScrollContainer
from settings.mechas.default_details_pool import DEFAULT_DETAILS_POOL_SETTINGS, DEFAULT_START_DETAILS
from stages.play_stage.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from stages.play_stage.round_lobby_stage.ui_elements.detail_pool_ui_obj import DetailUIElement
from game_logic.components.pools.details_pool import DetailsPool


class DetailPoolSettings(ScrollContainer):
    def __init__(self, pool_setting: dict, details_pool: DetailsPool):
        super().__init__(
            x=LobbyWindowsSizes.DetailsPoolSettings.X,
            y=LobbyWindowsSizes.DetailsPoolSettings.Y,
            size_x=LobbyWindowsSizes.DetailsPoolSettings.X_SIZE,
            size_y=LobbyWindowsSizes.DetailsPoolSettings.Y_SIZE,
            screen=MAIN_SCREEN,
        )
        self.pool_settings: dict = pool_setting
        self.details_pool: DetailsPool = details_pool
        self.build()
        self.render()

    def build(self):
        for k, v in self.pool_settings.items():
            name = self.details_pool.get_class_by_name(k).name
            self.add_detail(f'{name}:{v}')

    def add_detail(self, name):
        self.ui_objects.append(DetailUIElement(self.surface, name))

    def draw(self, dx=0, dy=0):
        for obj in self.ui_objects:
            obj.draw()
        self._screen.blit(self.surface, (dx + self.x0, dy + self.y0))
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1)
