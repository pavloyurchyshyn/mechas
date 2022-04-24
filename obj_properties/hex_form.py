from obj_properties.collide_interfaces import CollideInterface
from math import cos, sin, sqrt, dist, radians
from constants.properties import CIRCLE_TYPE, RECT_TYPE, LINE_TYPE, POINT_TYPE, HEXAGON_TYPE


class Hexagon(CollideInterface):
    DOT_NUM = 6
    FORM_TYPE = HEXAGON_TYPE

    def __init__(self, x, y, size):
        self._original_pos = x, y
        self._original_size = size
        self._size = self._width = self._height = self._inner_circle_r = self._lt = self._distance = self._center = None
        self._dots = []

        self.build(x, y, size)
        self._collide_able = 1

    def scale(self, scale_value):
        # self._center = self._original_pos[0]*scale_value, self._original_pos[1]*scale_value
        self.build(self._original_pos[0] * scale_value, self._original_pos[1] * scale_value,
                   self._original_size * scale_value)

    def _change_position(self, xy: list, *args, **kwargs) -> None:
        self.build(*xy, self._size)

    def build(self, x, y, size):
        self._lt = x, y
        self._size = size
        self._width = self._size * 2
        self._height = sqrt(3) * self._size
        self._inner_circle_r = self._height / 2
        self._distance = self._width * 3 / 4

        self._center = x + self._size, y + self._height / 2

        self.__make_dots()

    @property
    def left_top(self):
        return self._lt

    @property
    def size(self):
        return self._size

    @property
    def x(self):
        return self._center[0]

    @property
    def y(self):
        return self._center[1]

    def collide_dots(self, other) -> bool:
        for dot in other._dots:
            if self.collide_point(dot):
                return True

        return False

    def collide_point(self, xy: list) -> bool:
        return dist(xy, self._center) <= self._inner_circle_r

    def collide_circle(self, xy: list, R: int) -> bool:
        return dist(xy, self._center) <= self._size + R

    def collide(self, other) -> bool:
        """
        Returns True if collide object

        :param other:
        :return: bool
        """

        if self._collide_able:
            if other.FORM_TYPE == self.FORM_TYPE:
                return self.collide_hex(other)

            elif other.FORM_TYPE == RECT_TYPE:
                return other.collide_circle(self._center, self._size)

            elif other.FORM_TYPE == LINE_TYPE:
                return other.collide_circle(self._center, self._size)

            elif other.FORM_TYPE == POINT_TYPE:
                return self.collide_point(other._center)

            elif other.FORM_TYPE == CIRCLE_TYPE:
                return self.collide_circle(other._center, other._size)

            return self.collide_dots(other)
        else:
            return 0

    def collide_hex(self, other):
        return dist(self._center, other._center) <= self._distance and dist((0, self._center[1]),
                                                                            (0, other._center[1]) <= self._height / 2)

    def __make_dots(self):
        self._dots.clear()
        self._dots.append(self._center)

        x0, y0 = self._center

        for i in range(6):
            angle_rad = radians(60 * i)
            self._dots.append((int(x0 + self._size * cos(angle_rad)),
                               int(y0 + self._size * sin(angle_rad))))

    def get_size(self):
        return self._size

    def get_pos(self):
        return self._center

    @property
    def dots(self):
        if self._collide_able:
            return self._dots

        return ()

    @property
    def distance(self):
        return self._distance

    @property
    def inner_circle_r(self):
        return self._inner_circle_r

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height