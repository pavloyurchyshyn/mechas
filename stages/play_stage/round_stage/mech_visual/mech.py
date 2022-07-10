from pygame.draw import circle as draw_circle
from visual.main_window import MAIN_SCREEN
from mechas.base.mech import BaseMech
from stages.play_stage.round_stage.windows.world_window.visual_world import VisualWorld


class MechVisual:
    def __init__(self, mech: BaseMech, world: VisualWorld):
        self.mech = mech
        self.world = world

    def draw(self):
        tile = self.world.get_tile_by_coords(self.mech.position)
        if tile:
            pos = tile.get_pos()
            draw_circle(MAIN_SCREEN, (255, 255, 0), pos, 10)
        else:
            raise Exception(f'No pos: {self.mech.position}')