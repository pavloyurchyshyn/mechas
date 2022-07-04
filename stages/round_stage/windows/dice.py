from obj_properties.rect_form import Rectangle
from pygame.draw import rect as draw_rect
from pygame.draw import circle as draw_circle
from stages.round_stage.settings.windows_sizes import RoundSizes
from visual.main_window import MAIN_SCREEN
from visual.sprites_functions import get_surface


class DiceWindow(Rectangle):
    _dice_values = {
        1: (0,), 2: (-1, 4),
        3: (0, -1, 4), 4: (1, 3, 5, 7),
        5: (0, 1, 3, 5, 7), 6: (1, 2, 3, 5, 6, 7),
    }

    def __init__(self):
        super(DiceWindow, self).__init__(x=RoundSizes.Dice.X, y=RoundSizes.Dice.Y,
                                         size_x=RoundSizes.Dice.X_SIZE,
                                         size_y=RoundSizes.Dice.Y_SIZE)
        self.dice_rect = self.size_x * 0.2, self.size_y * 0.1, self.size_x * 0.6, self.size_x * 0.6
        self.dice_dots = Rectangle(*self.dice_rect).scale(0.5).dots
        self.dice_sprites: dict = {}
        self.current_dice_number = 5
        self.build_sprites()

    def build_sprites(self):
        for i, dots_pos in self._dice_values.items():
            sprite = get_surface(*self.sizes, transparent=1, color=(0, 0, 0, 0))
            draw_rect(sprite, (255, 255, 255), self.dice_rect, 0, 10)
            draw_rect(sprite, (50, 50, 50), self.dice_rect, 1, 10)
            for d in dots_pos:
                draw_circle(sprite, (0, 0, 0), self.dice_dots[d], 5)
            self.dice_sprites[i] = sprite

    def set_number(self, i):
        self.current_dice_number = i

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
        MAIN_SCREEN.blit(self.dice_sprites[self.current_dice_number], self.left_top)
