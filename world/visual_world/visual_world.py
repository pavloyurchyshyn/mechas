from obj_properties.hex_form import Hexagon

from constants.world_types import DIAMOND

from pygame.draw import lines as draw_lines
from pygame.draw import polygon as draw_polygon

from common.sprites_functions import get_surface
from settings.UI_setings.menus_settings.round_menu.arena_window import MIN_SCALE, MAX_SCALE, HEX_SIZE

from visual.font_loader import DEFAULT_FONT


class VisualHex(Hexagon):
    def __init__(self, x, y, size, surface=None, indexes=None):
        self._indexes = indexes
        self._surface = surface
        super().__init__(x=x, y=y + 1, size=size)

        if indexes:
            self.draw_img()

    def draw_img(self):
        self._img = get_surface(self._width, self._height, transparent=1)
        draw_polygon(self._img, (100, 100, 100), Hexagon(0, 0, self._size).dots[1:])
        c = DEFAULT_FONT.render(str(self._indexes), 1, (255, 255, 255), 1)
        x, y = self._img.get_rect().center
        self._img.blit(c, (x - c.get_width() / 2, y - c.get_height() / 2))

    def draw(self):
        draw_lines(self._surface, (255, 255, 255), 1, self._dots[1:], 4)
        self._surface.blit(self._img, self.left_top)
        draw_lines(self._surface, (255, 255, 255), 1, self._dots[1:], 2)

    def draw_bold(self):
        draw_lines(self._surface, (255, 255, 255), 1, self.dots[1:], 3)


class VisualWorld:
    def __init__(self):
        self._hex_size = HEX_SIZE

        self._arena = None
        self._even = None

        self._hex_example = None
        # hexes with current scale size
        self._hexes = []

        self._coordinates_hex_dict = {}

        self._image = None

        self._rect = (0, 0, 0, 0)
        self._left_hex = None
        self._right_hex = None
        self._top_hex = None
        self._bot_hex = None
        self._x_size = None
        self._y_size = None

    def draw(self):
        for h in self._hexes:
            h.draw()

    def build_world_img(self):
        self._image = get_surface(self._x_size, self._y_size, transparent=1)
        for h in self._hexes:
            h._surface = self._image
            h.draw()

    def get_cell_by_coordinates(self, coordinates):
        return self._coordinates_hex_dict.get(coordinates)

    def build_from_list(self, arena: list = DIAMOND, even: bool = False):
        self._hexes.clear()

        self._arena = arena
        self._even = even

        self._hex_example = VisualHex(0, 0, self._hex_size)

        for y, line in enumerate(arena):
            for x, val in enumerate(arena[y]):
                if val:
                    yp = y * self._hex_example.height + (self._hex_example.height // 2 * self.get_step(x))
                    xp = x * self._hex_example.distance

                    h = VisualHex(xp, yp, size=self._hex_size, indexes=(x, y))
                    self._hexes.append(h)
                    self._coordinates_hex_dict[(x, y)] = h

        self.define_edge_hexes_and_sizes()
        self.build_world_img()

    def define_edge_hexes_and_sizes(self):
        self._left_hex = self.get_left_hex()
        self._right_hex = self.get_right_hex()
        self._top_hex = self.get_top_hex()
        self._bot_hex = self.get_bot_hex()
        self._x_size = self.get_world_x_size()
        self._y_size = self.get_world_y_size()

    # ---------- current scale hexes ----------------------
    def get_left_hex(self) -> VisualHex:
        return min(self._hexes, key=lambda h: h.x)

    def get_right_hex(self) -> VisualHex:
        return max(self._hexes, key=lambda h: h.x)

    def get_top_hex(self) -> VisualHex:
        return min(self._hexes, key=lambda h: h.y)

    def get_bot_hex(self) -> VisualHex:
        return max(self._hexes, key=lambda h: h.y)

    def get_world_x_size(self):
        left = self._left_hex
        right = self._right_hex

        x0 = left.x - left.size
        x1 = right.x + right.size

        return x1 - x0 + 2

    def get_world_y_size(self):
        top = self._top_hex
        bot = self._bot_hex

        y0 = top.y - top.inner_circle_r
        y1 = bot.y + bot.inner_circle_r

        return y1 - y0 + 2

    @property
    def left_top(self):
        return self._left_hex.x - self._left_hex.size, self._top_hex.y - self._top_hex.inner_circle_r

    def get_world_rect(self):
        left = min(self._hexes, key=lambda h: h.x)
        x0 = left.x - left.size
        top = min(self._hexes, key=lambda h: h.y)
        y0 = top.y - top.inner_circle_r

        return x0, y0, self.get_world_x_size(), self.get_world_y_size()

    # ======================================================

    def scale(self, value):
        self._hex_example.scale(value)

        size = self._hex_example.size
        height = self._hex_example.height
        distance = self._hex_example.distance

        for h in self._hexes:
            x, y = h._indexes

            yp = y * height + (height // 2 * self.get_step(x))
            xp = x * distance

            h.build(xp, yp, size)
            h.draw_img()

        self.define_edge_hexes_and_sizes()
        self.build_world_img()

    def get_step(self, x):
        if self._even:
            return 0 if x % 2 else 1
        else:
            return 1 if x % 2 else 0

    def make_hex_with_coords(self, x, y):
        if (x, y) not in self._coordinates_hex_dict:
            return None

        if self._even:
            step = 0 if x % 2 else 1
        else:
            step = 1 if x % 2 else 0

        yp = y * self._hex_example.height + (self._hex_example.height // 2 * step)
        xp = x * self._hex_example.distance
        return Hexagon(xp, yp, self._hex_example.size)

    def close_cell(self, coordinates):
        self._coordinates_hex_dict[coordinates].close()

    def get_collide_hex(self, point):
        for h in self._hexes:
            if h.collide_point(point):
                return h

    def convert_coordinates_to_indexes(self, x, y):
        x = x // self._hex_example.distance
        y = (y - (self._hex_example.height // 2 * self.get_step(x))) // self._hex_example.height
        return x, y

    def normalize_coordinates(self, x, y):
        x, y = self.convert_coordinates_to_indexes(x, y)
        yp = y * self._hex_example.height + (self._hex_example.height // 2 * self.get_step(x))
        xp = x * self._hex_example.distance
        return xp, yp

    @property
    def image(self):
        return self._image


if __name__ == '__main__':
    pass
