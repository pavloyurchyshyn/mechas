from pygame.draw import rect as draw_rect
from obj_properties.rect_form import Rectangle

from visual.sprites_functions import get_surface
from common.global_mouse import GLOBAL_MOUSE

from visual.main_window import MAIN_SCREEN

from game_logic.stages.round_stage.windows.world_window.visual_world import VisualWorld
from game_logic.stages.round_stage.settings.windows_sizes import RoundSizes
from game_logic.stages.round_stage.settings.arena_window import *


class ArenaWindow(Rectangle):
    min_scale = MIN_SCALE
    max_scale = MAX_SCALE
    scale_speed = SCALE_SPEED

    arrow_speed = 1

    def __init__(self, x=RoundSizes.WorldWindow.X, y=RoundSizes.WorldWindow.Y,
                 size_x=RoundSizes.WorldWindow.X_SIZE, size_y=RoundSizes.WorldWindow.Y_SIZE):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self._current_scale = 1
        self._surf_pos = [self.x0, self.y0]

        self.visual_world = VisualWorld(self.get_rect())
        self._world_surface = get_surface(self.size_x, self.size_y)

        self._current_hex = None

    def update(self):
        if self.collide_point(GLOBAL_MOUSE.pos):
            pass

    def __check_for_scroll(self):
        if GLOBAL_MOUSE.scroll_top:
            self._current_scale += self.scale_speed
            if self._current_scale > self.max_scale:
                self._current_scale = self.max_scale
        elif GLOBAL_MOUSE.scroll_bot:
            self._current_scale -= self.scale_speed
            if self._current_scale < self.min_scale:
                self._current_scale = self.min_scale

    def draw(self):
        # MAIN_SCREEN.blit(self._world_surface, self.left_top)

        self.visual_world.draw_markup()
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
        # MAIN_SCREEN.blit(self.visual_world.image, self.left_top)
