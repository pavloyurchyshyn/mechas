from obj_properties.hex_form import Hexagon
from settings.logic_world.tile import HEX_SIZE


class WorldTile(Hexagon):
    def __init__(self, x, y, indexes: tuple, opened=True, size=HEX_SIZE, **kwargs):
        super().__init__(x=x, y=y, size=size)

        self._indexes = indexes

        self._walkable: int = kwargs.get('walkable', 1)

        self._opened = opened

        self._neighbours = []

    @property
    def is_open(self):
        return self._opened

    def open(self):
        self._opened = True

    def close(self):
        self._opened = False

    def add_neighbour(self, cell):
        self._neighbours.append(cell)

    @property
    def walkable(self):
        return self._walkable

    @property
    def indexes(self):
        return self._indexes

    @property
    def x(self):
        return self._indexes[0]

    @property
    def y(self):
        return self._indexes[1]
