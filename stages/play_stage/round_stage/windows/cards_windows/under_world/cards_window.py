from mechas.base.mech import BaseMech
from stages.play_stage.round_stage.windows.cards_windows.under_world.available_skills import UnusedSkillCards
from stages.play_stage.round_stage.windows.cards_windows.under_world.used_skills import UsedSkillsCards
from stages.play_stage.round_stage.windows.cards_windows.cards_factory import CardsFactory
from visual.skill_card import SkillCard


class CardsWindow:

    def __init__(self, mech: BaseMech):
        self.    cards_factory = CardsFactory(SkillCard)

        self.mech: BaseMech = mech
        self.skill_cards_win = UnusedSkillCards()
        self.used_skill_cards_win = UsedSkillsCards()

        self.update_skills_cards()

    def update_skills_cards(self):
        self.skill_cards_win.clear()
        for skill in self.mech.skills:
            # TODO add call of cards factory
            self.skill_cards_win.add_card(self.cards_factory.create_card(skill))

    def draw(self):
        self.skill_cards_win.draw()
        self.used_skill_cards_win.draw()
