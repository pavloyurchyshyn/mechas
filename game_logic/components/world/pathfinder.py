# from world.world import World


def path_carrier(func):
    cache = {}

    def wrapper(target_pos, current_pos):
        if (target_pos, current_pos) in cache:
            return cache[(target_pos, current_pos)]

        res = func(target_pos, current_pos)

        cache[(target_pos, current_pos)] = res

        return res

    return wrapper


class Pathfinder:
    def __init__(self, world):
        # self.__world: World = world
        self.__world_maze = world.maze.copy()
        self.__grid: Grid = Grid(matrix=self.__world_maze)
        self.__pathfinder: AStarFinder = AStarFinder(diagonal_movement=DiagonalMovement.always,
                                                     # max_runs=MAX_PATHFINDER_STEPS, time_limit=MAX_PATHFINDER_TIME
                                                     )
        self.path: list = None

    def current_path_going_to_target(self, target_position) -> bool:
        if self.path:
            return self.__world.scale_coors_for_pathfinder(*target_position) == self.path[-1]
        else:
            return 0

    def stop(self):
        self.path = None

    def get_next_step(self):
        if self.path:
            return self.__world.scale_coords_to_normal(*self.path[0])
        else:
            return None

    def get_step_position(self):
        x, y = self.path.pop(0)
        if not self.path:
            self.stop()

        return self.__world.scale_coords_to_normal(x, y)

    def build_path(self, target_pos, current_pos):
        if target_pos is None:
            self.stop()
            return

        if self.current_path_going_to_target(target_pos):
            return

        target_pos = self.__world.scale_coors_for_pathfinder(*target_pos)
        current_pos = self.__world.scale_coors_for_pathfinder(*current_pos)
        self.path = self._find_path(target_pos=target_pos, current_pos=current_pos)

        if not self.path:
            self.path = None

    def update_grid(self):
        if self.__world_maze != self.__world.maze:
            self.__world_maze = self.__world.maze.copy()
            self.__grid = Grid(matrix=self.__world_maze)

    # @path_carrier
    def _find_path(self, target_pos, current_pos):
        self.__grid.cleanup()

        end = self.__grid.node(*target_pos)
        start = self.__grid.node(*current_pos)
        path, runs = self.__pathfinder.find_path(start=start, end=end, grid=self.__grid)

        return path

    def __raise_coord(self, coord):
        return self.__world.scale_coords_to_normal(*coord)

    @property
    def raised_path(self):
        return list(map(self.__raise_coord, self.path))


if __name__ == '__main__':
    matrix = [
        [1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
    ]

    from game_logic.components.world import World
    from constants.world_types import DIAMOND
    from pathfinding.finder.a_star import AStarFinder
    from pathfinding.core.grid import Grid
    from pathfinding.core.diagonal_movement import DiagonalMovement
    world = World()
    world.build_from_list(DIAMOND, False)
    # grid = Grid(matrix=matrix)
    # print(grid.grid_str())
    # pathfinder = AStarFinder(DiagonalMovement.always)
    # print(pathfinder.find_path(grid.node(0, 0), grid.node(2, 2), grid))

    grid = Grid(matrix=world._path_finder_grid)

    start = grid.node(0, 0)
    end = grid.node(5, 2)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    print(path, runs)
    print(grid.grid_str(path=path))
