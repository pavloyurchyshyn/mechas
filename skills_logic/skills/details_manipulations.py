from skills_logic.base.skill import BaseSkill
from settings.skills.details_manipulations import DisconnectDetail, SwitchDetail


class DisconnectDetailSkill(BaseSkill):
    def __init__(self, unique_id):
        super(DisconnectDetailSkill, self).__init__(unique_id=unique_id, spell_cost=0, cooldown=0)

    def use(self, *args, **kwargs):
        # TODO
        pass