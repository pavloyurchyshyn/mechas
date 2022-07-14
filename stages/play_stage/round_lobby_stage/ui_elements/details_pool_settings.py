from visual.UI_base.obj_scroll_container_UI import ScrollContainer
from settings.mechas.default_details_pool import DEFAULT_DETAILS_POOL_SETTINGS, DEFAULT_START_DETAILS
from stages.play_stage.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from stages.play_stage.round_lobby_stage.ui_elements.detail_pool_ui_obj import DetailUIElement
from game_logic.components.pools.details_pool import DetailsPool
from common.global_mouse import GLOBAL_MOUSE


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
            self.add_detail(self.details_pool.get_class_by_name(k))

    def add_detail(self, detail_class):
        self.ui_objects.append(DetailUIElement(self.surface, detail_class, self.pool_settings))

    def update(self):
        self.check_for_scroll()

        clicked = False
        x, y = GLOBAL_MOUSE.x - self.x0, GLOBAL_MOUSE.y - self.y0

        for player_ui_obj in self.ui_objects.copy():
            player_ui_obj.update((x, y))
            if GLOBAL_MOUSE.lmb and not clicked:
                clicked = player_ui_obj.click((x, y))

    def draw(self, dx=0, dy=0):
        for obj in self.ui_objects:
            obj.draw()
        self._screen.blit(self.surface, (dx + self.x0, dy + self.y0))
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1)
