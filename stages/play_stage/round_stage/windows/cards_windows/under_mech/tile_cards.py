from obj_properties.rect_form import Rectangle
from pygame.draw import rect as draw_rect
from pygame import draw
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes
from visual.main_window import MAIN_SCREEN
from settings.global_parameters import test_draw_status_is_on
from constants.colors import simple_colors
from visual.cards.skill_card import SkillCard


# TODO
class TileCards(Rectangle):
    def __init__(self,
                 x=RoundSizes.TileCards.X, y=RoundSizes.TileCards.Y,
                 size_x=RoundSizes.TileCards.X_SIZE, size_y=RoundSizes.TileCards.Y_SIZE):
        super(TileCards, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.orig_card_x_size = self.card_x_size = self.size_x * 0.1
        self.orig_card_y_size = self.card_y_size = self.size_y * 0.8
        self.right_border_step = self.size_x * 0.01
        self.card_y_pos = self.y0 + (self.size_y - self.orig_card_y_size) // 2

        self.card_rect = self.right_border_step, self.card_y_pos, self.card_x_size, self.card_y_size

        self.cards = []

    def add_card(self, card: SkillCard):
        self.cards.append(card)
        self.calculate_cards_positions()

    def remove_card(self, card: SkillCard):
        self.cards.remove(card)
        self.calculate_cards_positions()

    def clear(self):
        self.cards.clear()

    def calculate_cards_positions(self):
        # place for cards with step from borders
        w_space = self.size_x - self.right_border_step - self.right_border_step
        cards_num = len(self.cards)
        # size for all cards
        sum_width = cards_num * self.card_x_size
        step_between_cards = 0
        size_scale = 1

        if w_space > sum_width:
            step_between_cards = 2
        else:
            size_scale = (w_space - self.card_x_size // 2) / sum_width

        step_w = (cards_num - 1) * step_between_cards
        x = self.x0 + self.size_x // 2 - step_w - sum_width // 2 * size_scale - self.right_border_step

        for card in self.cards:
            card.change_position_lt((x, self.card_y_pos))
            x += self.card_x_size * size_scale + step_between_cards

    def update(self):
        pass

    def draw(self):
        draw_rect(MAIN_SCREEN, (0, 255, 0), self.get_rect(), 1, 5)
        for card in self.cards:
            card.draw()

        if test_draw_status_is_on():
            color = simple_colors.yellow
            for dotx, doty in self._dots[1:]:
                draw.circle(MAIN_SCREEN, color, (dotx, doty), 2)
