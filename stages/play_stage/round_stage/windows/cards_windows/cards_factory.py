# TODO class to craft card according to skill
from skills.base.skill import BaseSkill
from visual.skill_card import SkillCard


class CardsFactory:
    """
    Factory of visual cards.
    """
    def __init__(self, card_class):
        self.cards_class = card_class
        self.memory = {}

    def get_card_by_skill(self, skill: BaseSkill) -> SkillCard:
        return self.get_card(skill.unique_id)

    def get_card(self, id) -> SkillCard:
        return self.memory.get(id)

    def create_card(self, skill: BaseSkill) -> SkillCard:
        if skill.unique_id in self.memory:
            return self.get_card(skill.unique_id)

        card = self.cards_class(skill)

        self.memory[skill.unique_id] = card

        return card

    def clear(self):
        self.memory.clear()