from obj_properties.rect_form import Rectangle
from obj_properties.hex_form import Hexagon

from common.sprites_functions import get_surface
from common.global_mouse import GLOBAL_MOUSE

from world.visual_world.visual_world import VisualWorld

from visual.main_window import MAIN_SCREEN
from settings.UI_setings.menus_settings.round_menu.arena_window import *

from pygame.draw import lines as draw_lines
from pygame.draw import circle as draw_circle


class ArenaWindow(Rectangle):
    min_scale = MIN_SCALE
    max_scale = MAX_SCALE
    scale_speed = SCALE_SPEED

    def __init__(self, x=X_POS, y=Y_POS, size_x=X_SIZE, size_y=Y_SIZE):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self._current_scale = 1
        self._surf_pos = [self.x0, self.y0]

        self._visual_world = VisualWorld()
        self._visual_world.build_from_list()
        self._world_surface = get_surface(self.size_x, self.size_y)
        self.update_scale_world(force=True)

        self._current_hex = Hexagon(0, 0, 0)

    def update(self):
        if self.collide_point(GLOBAL_MOUSE.pos):
            self.update_scale_world()

            self.update_hex_border()

    def update_hex_border(self):
        x, y = GLOBAL_MOUSE.pos

        h: Hexagon = self._visual_world.get_collide_hex(
            (x - self._surf_pos[0] - self.x0, y - self._surf_pos[1] - self.y0))
        if h:
            # draw_lines(MAIN_SCREEN, (0, 0, 255), 1, h._dots[1:], 3)
            x, y = h.left_top
            self._current_hex.build(x + self._surf_pos[0] + self.x0, y + self._surf_pos[1] + self.y0, h.size)

    def update_scale_world(self, force=False):
        s_val = self._current_scale

        if GLOBAL_MOUSE.scroll_top:
            self._current_scale += self.scale_speed
            if self._current_scale > self.max_scale:
                self._current_scale = self.max_scale
        elif GLOBAL_MOUSE.scroll_bot:
            self._current_scale -= self.scale_speed
            if self._current_scale < self.min_scale:
                self._current_scale = self.min_scale

        if s_val != self._current_scale or force:
            self._world_surface.fill((0, 0, 0))
            self._visual_world.scale(self._current_scale)

            x_mouse_pos, y_mouse_pos = GLOBAL_MOUSE.pos

            self._surf_pos = [1, 1]
            img_x_size, img_y_size = self._visual_world._image.get_size()
            if img_x_size < self.size_x:
                self._surf_pos[0] += (self.size_x - img_x_size) / 2
            if img_y_size < self.size_y:
                self._surf_pos[1] += (self.size_y - img_y_size) / 2

            if img_x_size > self.size_x:
                self._surf_pos[0] -= (img_x_size - self.x1) / 2
                rel_pos_x = (self._surf_pos[0] + img_x_size / 2 - x_mouse_pos) / self.size_x
                self._surf_pos[0] += img_x_size / 2 * rel_pos_x

            if img_y_size > self.size_y:
                self._surf_pos[1] -= (img_y_size - self.y1) / 2
                rel_pos_y = (self._surf_pos[1] + img_y_size / 2 - y_mouse_pos) / self.size_y
                self._surf_pos[1] += img_y_size / 2 * rel_pos_y

            self._world_surface.blit(self._visual_world.image, self._surf_pos)

    def draw(self):
        MAIN_SCREEN.blit(self._world_surface, self.left_top)

        draw_lines(MAIN_SCREEN, (200, 200, 255), 1, self._current_hex._dots[1:], 5)
