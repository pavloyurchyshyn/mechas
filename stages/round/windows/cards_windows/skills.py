from obj_properties.rect_form import Rectangle
from pygame.draw import rect as draw_rect
from pygame import draw
from stages.round.settings.windows_sizes import RoundSizes
from visual.main_window import MAIN_SCREEN
from visual.skill_card import SkillCard
from settings.global_parameters import test_draw_status_is_on
from constants.colors import simple_colors


class UnsedSkillCards(Rectangle):
    def __init__(self, x=RoundSizes.SkillsCards.X, y=RoundSizes.SkillsCards.Y,
                 size_x=RoundSizes.SkillsCards.X_SIZE, size_y=RoundSizes.SkillsCards.Y_SIZE):
        super(UnsedSkillCards, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.orig_card_x_size = self.card_x_size = self.size_x * 0.1
        self.orig_card_y_size = self.card_y_size = self.size_y * 0.8
        self.right_border_step = self.size_x * 0.01
        self.card_y_pos = self.y0 + (self.size_y - self.orig_card_y_size)//2

        self.cards = []

        # for i in range(1):
        #     self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))

    def add_card(self, card):
        self.cards.append(card)
        self.calculate_cards_positions()

    def remove_card(self, card):
        self.cards.remove(card)
        self.calculate_cards_positions()

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
            size_scale = (w_space - self.card_x_size//2) / sum_width

        step_w = (cards_num - 1) * step_between_cards
        x = self.x0 + self.size_x//2 - step_w - sum_width//2 * size_scale - self.right_border_step

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
