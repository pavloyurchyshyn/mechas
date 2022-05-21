__all__ = ['WorldsConstants', 'WorldsNames']


class WorldsNames:
    Diamond = 'Diamond'
    Cube = 'Cube'


class WorldInterface:
    Name = None
    Map = None
    Even = True
    Description = ''


class WorldsConstants:
    __names = ['DiamondWorld', 'CubeWorld']

    @classmethod
    def get_world_by_name(cls, name):
        for n in cls.__names:
            world: WorldInterface = getattr(cls, n)
            if world.Name == name:
                return world

    class DiamondWorld(WorldInterface):
        Name = WorldsNames.Diamond
        Even = False
        Map = [
            # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
            [0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0],  # 1
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 2
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 3
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 4
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 5
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 6
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 7
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 8
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 9
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 10
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # 11
        ]

    class CubeWorld(WorldInterface):
        Name = WorldsNames.Cube
        Even = False
        Map = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]
