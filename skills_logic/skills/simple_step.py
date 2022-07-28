from skills_logic.base.skill import BaseSkill
from skills_logic.base.exceptions import OnCooldownException
from mechas.base.mech import BaseMech
from settings.skills.simple_step import SimpleStepAttrs


class SimpleStep(BaseSkill):
    name = SimpleStepAttrs.name
    verbal_name = SimpleStepAttrs.verbal_name

    def __init__(self, unique_id):
        super(SimpleStep, self).__init__(unique_id=unique_id,
                                         spell_cost=SimpleStepAttrs.spell_cost,
                                         cooldown=SimpleStepAttrs.cooldown)

    def use(self, mech, new_pos, *args, **kwargs):
        if not self.on_cooldown():
            mech: BaseMech = kwargs.get('mech')
            mech.change_position(kwargs.get('new_pos'))
            mech.spend_energy(self.spell_cost)

        else:
            raise OnCooldownException
