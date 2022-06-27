from skills.base.skill import BaseSkill
from settings.skills.simple_step import SimpleStepAttrs


class SimpleStep(BaseSkill):
    name = SimpleStepAttrs.name

    def __init__(self):
        super(SimpleStep, self).__init__(spell_cost=SimpleStepAttrs.spell_cost,
                                         cooldown=SimpleStepAttrs.cooldown)

    def use(self, *args, **kwargs):