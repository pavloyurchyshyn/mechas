from constants.world_types import WorldsConstants, WorldsNames
from settings.logic_world.tile import HEX_SIZE


class AbstractWorld:
    def __init__(self, world_name: dict = WorldsNames.Diamond, tile_size=HEX_SIZE):
        self.data = WorldsConstants.get_world_by_name(world_name)
        self.tiles = []
        self.tiles_dict = {}
        self.vertical_count = 0
        self.horizontal_count = 0
        self.tile_size = tile_size

        self.define_sizes()

    def define_sizes(self):
        self.vertical_count = len(self.data.Map)
        self.horizontal_count = len(max(self.data.Map, key=lambda a: len(a)))

    def get_step(self, x):
        if self.data.Even:
            return 0 if x % 2 else 1
        else:
            return 1 if x % 2 else 0
