from skills_logic.base.skill import BaseSkill
from visual.cards.base_card import BaseCard
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes

__all__ = ['SkillCard', ]


class SkillCard(BaseCard):
    def __init__(self, skill: BaseSkill,
                 x=RoundSizes.CardSize.X,
                 y=RoundSizes.CardSize.Y,
                 size_x=RoundSizes.CardSize.X_SIZE,
                 size_y=RoundSizes.CardSize.Y_SIZE,
                 ):

        self.skill: BaseSkill = skill

        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y,
                         title_text=self.skill.verbal_name,
                         unique_id=self.skill.unique_id)

    def update(self):
        pass

