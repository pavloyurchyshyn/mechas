from world.visual_world import VisualWorld
from constants.world_types import DIAMOND
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement

world = VisualWorld()
world.build_from_list(DIAMOND, False)
# grid = Grid(matrix=matrix)
# print(grid.grid_str())
# pathfinder = AStarFinder(DiagonalMovement.always)
# print(pathfinder.find_path(grid.node(0, 0), grid.node(2, 2), grid))

grid = Grid(matrix=world._path_finder_grid)

start = grid.node(4, 1)
end = grid.node(7, 1)

finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
path, runs = finder.find_path(start, end, grid)
print(path, runs)
print(grid.grid_str(path=path, show_weight=True, path_chr='*', block_chr=' '))
print(grid.grid_str(path=None, show_weight=True, path_chr='*', block_chr=' '))
