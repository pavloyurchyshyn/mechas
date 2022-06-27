from mechas.base.parts.body import BaseBody
from mechas.base.parts.arm import BaseArm
from mechas.base.parts.leg import BaseLeg
from constants.mechas.detail_const import *
from settings.mechas.details_names import DetailNames


class MetalBody(BaseBody):
    name = DetailNames.SimpleMetal.Body

    def __init__(self, unique_id):
        data = {DetailsAttrs.EnergyRegen: 1, DetailsAttrs.AddEnergy: 10}
        super(MetalBody, self).__init__(unique_id=unique_id, damage=1, armor=1, **data)


class MetalArm(BaseArm):
    name = DetailNames.SimpleMetal.Arm

    def __init__(self, unique_id):
        super(MetalArm, self).__init__(unique_id=unique_id, damage=1, armor=1)


class MetalLeg(BaseLeg):
    name = DetailNames.SimpleMetal.Leg

    def __init__(self, unique_id):
        super(MetalLeg, self).__init__(unique_id=unique_id, damage=1, armor=1)
