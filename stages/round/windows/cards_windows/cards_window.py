from stages.round.windows.cards_windows.skills import UnsedSkillCards
from stages.round.windows.cards_windows.used_skills import UsedSkillsCards


class CardsWindow:
    def __init__(self):
        self.skill_cards_win = UnsedSkillCards()
        self.used_skill_cards_win = UsedSkillsCards()
        self.used_skill_cards_win.build_card_slots()

    def draw(self):
        self.skill_cards_win.draw()
        self.used_skill_cards_win.draw()