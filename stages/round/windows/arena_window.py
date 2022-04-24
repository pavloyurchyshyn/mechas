from obj_properties.rect_form import Rectangle
from obj_properties.hex_form import Hexagon

from common.sprites_functions import get_surface
from common.global_mouse import GLOBAL_MOUSE

from world.visual_world.visual_world import WorldMarkup

from visual.UI_base.button_UI import Button

from visual.main_window import MAIN_SCREEN
from settings.UI_setings.menus_settings.round_menu.arena_window import *

from pygame.draw import lines as draw_lines
from pygame.draw import line as draw_line
from pygame.draw import circle as draw_circle
from pygame.draw import rect as draw_rect


class ArenaWindow(Rectangle):
    min_scale = MIN_SCALE
    max_scale = MAX_SCALE
    scale_speed = SCALE_SPEED

    arrow_speed = 1

    def __init__(self, x=X_POS, y=Y_POS, size_x=X_SIZE, size_y=Y_SIZE):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self._current_scale = 1
        self._surf_pos = [self.x0, self.y0]

        self.visual_world = WorldMarkup()
        self.visual_world.build_from_list()
        self._world_surface = get_surface(self.size_x, self.size_y)
        self.scale_world()
        self.blit_into_window()

        self._current_hex = None

    def update(self):
        if self.collide_point(GLOBAL_MOUSE.pos):
            self.check_for_world_move()
            self.update_hex_border()

    def check_for_world_move(self):
        scale_val = self._current_scale
        self.__check_for_scroll()

        if scale_val != self._current_scale:
            self._surf_pos = [self.x0, self.y0]
            self.scale_world()
            self.blit_into_window()

    def scale_world(self):
        self.visual_world._hex_example.scale(self._current_scale)

        x_mouse_pos, y_mouse_pos = GLOBAL_MOUSE.pos

        img_x_size = self.get_visual_world_w()
        img_y_size = self.get_visual_world_h()

        # ----- if less than window -----------
        if img_x_size < self.size_x:
            self._surf_pos[0] += (self.size_x - img_x_size) / 2
        if img_y_size < self.size_y:
            self._surf_pos[1] += (self.size_y - img_y_size) / 2
        # ------ if bigger ---------------
        scrolled = any((GLOBAL_MOUSE.scroll_bot, GLOBAL_MOUSE.scroll_top))
        if img_x_size > self.size_x:
            self._surf_pos[0] -= (img_x_size - self.x1) / 2
            rel_pos_x = (self._surf_pos[0] + img_x_size / 2 - x_mouse_pos) / self.size_x
            self._surf_pos[0] += img_x_size / 2 * rel_pos_x

        if img_y_size > self.size_y:
            self._surf_pos[1] -= (img_y_size - self.y1) / 2
            rel_pos_y = (self._surf_pos[1] + img_y_size / 2 - y_mouse_pos) / self.size_y
            self._surf_pos[1] += img_y_size / 2 * rel_pos_y

        self.visual_world.scale(self._current_scale, *self._surf_pos)

    def get_visual_world_h(self):
        return self.visual_world._hex_example.height * self.visual_world._vertical_count

    def get_visual_world_w(self):
        return self.visual_world._hex_example.distance * self.visual_world._horizontal_count + self.visual_world._hex_example.size / 2

    def get_hex(self):
        return self.visual_world.get_collide_hex(GLOBAL_MOUSE.pos)

    def update_hex_border(self):
        h: Hexagon = self.get_hex()
        if h:
            self._current_hex = h

    def __check_for_scroll(self):
        if GLOBAL_MOUSE.scroll_top:
            self._current_scale += self.scale_speed
            if self._current_scale > self.max_scale:
                self._current_scale = self.max_scale
        elif GLOBAL_MOUSE.scroll_bot:
            self._current_scale -= self.scale_speed
            if self._current_scale < self.min_scale:
                self._current_scale = self.min_scale

    def blit_into_window(self):
        self._world_surface.fill((0, 0, 0))
        x, y = self._surf_pos
        y -= self.y0
        self._world_surface.blit(self.visual_world.image, (x, y))

    def draw(self):
        MAIN_SCREEN.blit(self._world_surface, self.left_top)

        if self._current_hex:
            points = self._current_hex._dots[1:]
            draw_lines(MAIN_SCREEN, (200, 200, 255), 1, points, 5)

        self.visual_world.draw_markup()
