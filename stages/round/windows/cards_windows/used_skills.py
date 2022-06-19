from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from pygame import draw
from stages.round.settings.windows_sizes import RoundSizes
from settings.global_parameters import test_draw_status_is_on
from constants.colors import simple_colors


class UsedCardSlot(Rectangle):
    def __init__(self, x, y, size_x, size_y):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.slot = None

    def set_slot_obj(self, obj):
        self.slot = obj

    def draw(self):
        if self.slot:
            self.slot.draw()

        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
        if test_draw_status_is_on():
            color = simple_colors.yellow
            for dotx, doty in self._dots[1:]:
                draw.circle(MAIN_SCREEN, color, (dotx, doty), 2)


class UsedSkillsCards(Rectangle):
    def __init__(self, x=RoundSizes.UsedSkillsCards.X, y=RoundSizes.UsedSkillsCards.Y,
                 size_x=RoundSizes.UsedSkillsCards.X_SIZE, size_y=RoundSizes.UsedSkillsCards.Y_SIZE):
        super(UsedSkillsCards, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.right_border_step = self.size_x * 0.05
        self.orig_card_x_size = self.card_x_size = self.size_x * 0.1
        self.orig_card_y_size = self.card_y_size = self.size_y * 0.8
        self.card_y_pos = self.y0 + (self.size_y - self.orig_card_y_size) // 2

        self.cards_num = 3
        self.slots = []
        self.build_slots()

    def build_slots(self):
        self.slots.clear()
        for i in range(self.cards_num):
            self.slots.append(UsedCardSlot(0, self.card_y_pos, self.orig_card_x_size, self.orig_card_y_size))

        self.calculate_cards_positions()

    def calculate_cards_positions(self):
        w_space = self.size_x - self.right_border_step - self.right_border_step
        cards_num = len(self.slots)
        sum_width = cards_num * self.card_x_size
        step_between_cards = 0
        size_scale = 1

        if w_space > sum_width:
            step_between_cards = (w_space - sum_width) / (cards_num - 1)
        else:
            size_scale = w_space / sum_width

        # working bad when 20+ cards #refactor
        step_w = (cards_num - 1) * step_between_cards
        x = self.x0 + (self.size_x - step_w - sum_width * size_scale) // 2

        for card in self.slots:
            card.change_position_lt((x, self.card_y_pos))
            x += self.card_x_size * size_scale + step_between_cards

    def update(self):
        pass

    def draw(self):
        for slot in self.slots:
            slot.draw()

        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)

        if test_draw_status_is_on():
            color = simple_colors.yellow
            for dotx, doty in self._dots[1:]:
                draw.circle(MAIN_SCREEN, color, (dotx, doty), 2)
