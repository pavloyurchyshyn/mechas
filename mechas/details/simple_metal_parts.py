from mechas.base.parts.body import BaseBody
from mechas.base.parts.arm import BaseArm
from mechas.base.parts.leg import BaseLeg

from skills_logic.skills.simple_step import SimpleStep

from constants.mechas.detail_const import *
from settings.mechas.details_names import DetailNames

__all__ = ['MetalArm', 'MetalLeg', 'MetalBody']


class MetalArm(BaseArm):
    name = DetailNames.SimpleMetal.Arm
    verbal_name = 'Metal Arm'

    def __init__(self, unique_id):
        super(MetalArm, self).__init__(unique_id=unique_id, damage=1, armor=1, add_hp=1, energy_regen=0.25)


class MetalLeg(BaseLeg):
    name = DetailNames.SimpleMetal.Leg
    verbal_name = 'Metal Leg'

    def __init__(self, unique_id):
        skills = (SimpleStep, )
        data = {
            DetailsAttrs.AddEnergy: 1,
            DetailsAttrs.HPRegen: 0.25,
            DetailsAttrs.AddHP: 1,
        }
        super(MetalLeg, self).__init__(unique_id=unique_id, damage=1, armor=1, skills=skills, **data)


class MetalBody(BaseBody):
    name = DetailNames.SimpleMetal.Body
    verbal_name = 'Metal Body'

    def __init__(self, unique_id):
        data = {DetailsAttrs.EnergyRegen: 1,
                DetailsAttrs.AddEnergy: 10,
                DetailsAttrs.AddHP: 10,
                DetailsAttrs.HPRegen: 1}
        super(MetalBody, self).__init__(unique_id=unique_id, damage=1, armor=1, **data)



