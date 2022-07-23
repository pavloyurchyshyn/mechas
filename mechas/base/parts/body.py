from mechas.base.parts.detail import BaseDetail
from mechas.base.slot import ArmSlot, LegSlot
from constants.mechas.detail_const import *

__all__ = ['BaseBody', ]


class BaseBody(BaseDetail):
    detail_type = DetailsTypes.BODY

    class Sides:
        LeftSlots = 'left_slots_classes'
        RightSlots = 'right_slots_classes'

    def __init__(self, unique_id=None, damage=0, armor=0, **kwargs):
        super(BaseBody, self).__init__(unique_id=unique_id, damage=damage, armor=armor, **kwargs)

        self.left_slots_classes = kwargs.get(BaseBody.Sides.LeftSlots, (ArmSlot, LegSlot))
        self.right_slots_classes = kwargs.get(BaseBody.Sides.RightSlots, (ArmSlot, LegSlot))

    def get_left_slots(self):
        return self.left_slots_classes

    def get_right_slots(self):
        return self.right_slots_classes

    @property
    def skills(self):
        return self._skills
