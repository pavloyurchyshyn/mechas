from mechas.base.mech import BaseMech
from visual.skill_card import SkillCard
from stages.play_stage.round_stage.windows.cards_windows.skills import UnusedSkillCards
from stages.play_stage.round_stage.windows.cards_windows.used_skills import UsedSkillsCards


class CardsWindow:
    def __init__(self, mech: BaseMech):
        self.mech: BaseMech = mech
        self.skill_cards_win = UnusedSkillCards()
        self.used_skill_cards_win = UsedSkillsCards()

        self.update_cards()

    def update_cards(self):
        self.skill_cards_win.clear()
        for skill in self.mech.skills:
            # TODO add call of cards factory
            self.skill_cards_win.add_card(SkillCard(*self.skill_cards_win.card_rect, skill=skill))

    def draw(self):
        self.skill_cards_win.draw()
        self.used_skill_cards_win.draw()
