class WorldCell:
    def __init__(self, coordinates: tuple, opened=True, **kwargs):
        self._coordinates = coordinates

        self._walkable: int = kwargs.get('walkable', 1)

        self._opened = opened

        self._neighbours = []

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
    def coordinates(self):
        return self._coordinates
