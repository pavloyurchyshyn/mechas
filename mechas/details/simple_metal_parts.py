from mechas.base.parts.body import BaseBody
from mechas.base.parts.arm import BaseArm
from mechas.base.parts.leg import BaseLeg
from mechas.base.slot import ArmSlot, LegSlot

from skills.simple_step import SimpleStep

from constants.mechas.detail_const import *
from settings.mechas.details_names import DetailNames

__all__ = ['MetalArm', 'MetalLeg', 'MetalBody']


class MetalArm(BaseArm):
    name = DetailNames.SimpleMetal.Arm

    def __init__(self, unique_id):
        super(MetalArm, self).__init__(unique_id=unique_id, damage=1, armor=1)


class MetalLeg(BaseLeg):
    name = DetailNames.SimpleMetal.Leg

    def __init__(self, unique_id):
        skills = (SimpleStep(), )
        super(MetalLeg, self).__init__(unique_id=unique_id, damage=1, armor=1, skills=skills)


class MetalBody(BaseBody):
    name = DetailNames.SimpleMetal.Body

    def __init__(self, unique_id):
        data = {DetailsAttrs.EnergyRegen: 1,
                DetailsAttrs.AddEnergy: 10,
                BodyInitAttrs.arm_class: ArmSlot,
                BodyInitAttrs.leg_class: LegSlot, }
        super(MetalBody, self).__init__(unique_id=unique_id, damage=1, armor=1, **data)


