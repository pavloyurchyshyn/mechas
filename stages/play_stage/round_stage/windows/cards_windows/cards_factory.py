# TODO class to craft card according to skill
from skills_logic.base.skill import BaseSkill
from mechas.base.parts.detail import BaseDetail
from visual.cards.skill_card import SkillCard
from visual.cards.details_card import DetailCard


class CardsFactory:
    """
    Factory of visual cards.
    """

    def __init__(self):
        self.skill_cards_class = SkillCard
        self.detail_cards_class = DetailCard
        self.memory = {}

    def get_card_by_skill(self, skill: BaseSkill) -> SkillCard:
        return self.get_card(skill.unique_id)

    def get_card(self, id):
        return self.memory.get(id)

    def create_skill_card(self, skill: BaseSkill) -> SkillCard:
        return self.create_card(self.skill_cards_class, skill)

    def create_detail_card(self, detail: BaseDetail) -> DetailCard:
        return self.create_card(self.detail_cards_class, detail)

    def create_card(self, card_class, obj):
        if obj.unique_id in self.memory:
            return self.get_card(obj.unique_id)

        card = card_class(obj)

        self.memory[obj.unique_id] = card

        return card

    def clear(self):
        self.memory.clear()
