from obj_properties.rect_form import Rectangle
from pygame.draw import rect as draw_rect
from settings.UI_setings.menus_settings.round_menu.windows_sizes import RoundSizes
from visual.main_window import MAIN_SCREEN
from visual.skill_card import SkillCard


class UnsedSkillCards(Rectangle):
    def __init__(self, x=RoundSizes.SkillsCards.X, y=RoundSizes.SkillsCards.Y,
                 size_x=RoundSizes.SkillsCards.X_SIZE, size_y=RoundSizes.SkillsCards.Y_SIZE):
        super(UnsedSkillCards, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.orig_card_x_size = self.card_x_size = self.size_x * 0.1
        self.orig_card_y_size = self.card_y_size = self.size_y * 0.6
        self.top_border_step = self.size_y * 0.05
        self.right_border_step = self.size_x * 0.05
        self.card_y_pos = self.y1 - self.card_y_size + self.top_border_step

        self.cards = [SkillCard(self.x0 + self.right_border_step, self.card_y_pos, self.card_x_size,
                                self.card_y_size, text='1')]

        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # # -------------------------------------11
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # # -------------------------------------21
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards)+1))
        #
        # # --------------------------------------31
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # self.add_card(SkillCard(0, self.card_y_pos, self.card_x_size, self.card_y_size, text=len(self.cards) + 1))
        # -----------------------------------40

    def add_card(self, card):
        self.cards.append(card)
        self.calculate_cards_positions()
        print(len(self.cards))

    def remove_card(self, card):
        self.cards.remove(card)
        self.calculate_cards_positions()

    def calculate_cards_positions(self):
        w_space = self.size_x - self.right_border_step - self.right_border_step
        cards_num = len(self.cards)
        sum_width = cards_num * self.card_x_size
        step_between_cards = 0
        size_scale = 1

        if w_space > sum_width:
            step_between_cards = 2
        else:
            size_scale = (w_space - self.card_x_size) / sum_width

        step_w = (cards_num - 1) * step_between_cards
        start_x = self.x0 + self.size_x / 2  # + self.right_border_step
        x = start_x - step_w / 2 - sum_width * size_scale / 2
        for card in self.cards:
            card.change_position((x, self.card_y_pos))
            x += self.card_x_size * size_scale + step_between_cards

    def update(self):
        pass

    def draw(self):
        draw_rect(MAIN_SCREEN, (0, 255, 0), self.get_rect(), 1)
        for card in self.cards:
            card.draw()
