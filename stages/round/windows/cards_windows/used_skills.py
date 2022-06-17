from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from stages.round.settings.windows_sizes import RoundSizes
from visual.UI_base.element_slot_UI import UIObjSlot


class UsedSkillsCards(Rectangle):
    def __init__(self, x=RoundSizes.UsedSkillsCards.X, y=RoundSizes.UsedSkillsCards.Y,
                 size_x=RoundSizes.UsedSkillsCards.X_SIZE, size_y=RoundSizes.UsedSkillsCards.Y_SIZE):
        super(UsedSkillsCards, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.cards_num = 3
        self.slots = []
        self.slot_size = (50, 50)

    def build_card_slots(self):
        for i in range(self.cards_num):
            self.slots.append(UIObjSlot(self.x0 + i * 70, self.y0, size_x=50))

    def update(self):
        pass

    def draw(self):
        for slot in self.slots:
            slot.draw()
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
