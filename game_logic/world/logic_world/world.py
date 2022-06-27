from game_logic.world.logic_world.tile import WorldTile
from constants.world_types import WorldsNames
from settings.logic_world.tile import HEX_SIZE
from game_logic.world.logic_world.abstract_world import AbstractWorld


class World(AbstractWorld):
    def __init__(self, world_name: dict = WorldsNames.Diamond, tile_size=HEX_SIZE):
        super().__init__(world_name, tile_size)

        self.build()

    def build(self):
        self.tiles.clear()

        world_data = self.data.Map

        tile_height = WorldTile.get_tile_height(self.tile_size)
        tile_distance = WorldTile.get_tile_distance(self.tile_size)
        for y, line in enumerate(world_data):
            for x, val in enumerate(world_data[y]):
                if val:
                    yp = y * tile_height + (tile_height // 2 * self.get_step(x))
                    xp = x * tile_distance

                    h = WorldTile(x=xp, y=yp, size=self.tile_size, indexes=(x, y))
                    self.tiles.append(h)
                    self.tiles_dict[(x, y)] = h

    def get_tile(self, coordinates):
        return self.tiles_dict[coordinates]

    def close_tile(self, coordinates):
        self.tiles_dict[coordinates].close()

    def open_tile(self, coordinates):
        self.tiles_dict[coordinates].open()
