from skills.base.skill import BaseSkill
from skills.base.exceptions import OnCooldownException
from mechas.base.mech import BaseMech
from settings.skills.simple_step import SimpleStepAttrs


class SimpleStep(BaseSkill):
    name = SimpleStepAttrs.name

    def __init__(self):
        super(SimpleStep, self).__init__(spell_cost=SimpleStepAttrs.spell_cost,
                                         cooldown=SimpleStepAttrs.cooldown)

    def use(self, mech, new_pos, *args, **kwargs):
        if not self.on_cooldown():
            mech: BaseMech = kwargs.get('mech')
            mech.change_position(kwargs.get('new_pos'))
            mech.spend_energy(self.spell_cost)

        else:
            raise OnCooldownException
