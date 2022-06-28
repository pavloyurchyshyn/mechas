from mechas.base.parts.detail import BaseDetail
from mechas.base.slot import ArmSlot, LegSlot, BaseSlot
from mechas.base.exceptions import SlotDoesntExistsError
from constants.mechas.detail_const import *

__all__ = ['BaseBody', ]


class BaseBody(BaseDetail):
    detail_type = DetailsTypes.BODY
    arm_slot_class: BaseSlot = ArmSlot
    leg_slot_class: BaseSlot = LegSlot

    class Sides:
        LeftArms = 'left_arms'
        RightArms = 'right_arms'
        LeftLegs = 'left_legs'
        RightLegs = 'right_legs'

        sides = (LeftArms, RightArms, LeftLegs, RightLegs)
        left_parts = (LeftArms, LeftLegs)
        right_parts = (RightArms, RightLegs)

    def __init__(self, unique_id=None, damage=0, armor=0, **kwargs):
        super(BaseBody, self).__init__(unique_id=unique_id, damage=damage, armor=armor, **kwargs)
        arm_slot_class = kwargs[BodyInitAttrs.arm_class] if kwargs.get(BodyInitAttrs.arm_class) else self.arm_slot_class
        leg_slot_class = kwargs[BodyInitAttrs.leg_class] if kwargs.get(BodyInitAttrs.leg_class) else self.leg_slot_class

        self.left_arms = {i: arm_slot_class(parent=self, num=i) for i in range(kwargs.get(BodyInitAttrs.LeftArmsNum, 1))}
        self.right_arms = {i: arm_slot_class(parent=self, num=i) for i in range(kwargs.get(BodyInitAttrs.RightArmsNum, 1))}
        self.left_legs = {i: leg_slot_class(parent=self, num=i) for i in range(kwargs.get(BodyInitAttrs.LeftLegsNum, 1))}
        self.right_legs = {i: leg_slot_class(parent=self, num=i) for i in range(kwargs.get(BodyInitAttrs.RightLegsNum, 1))}

    # ===== SET =================
    def set_left_arm(self, slot_id, arm):
        self.__set_detail(self.left_arms, slot_id, arm)

    def set_right_arm(self, slot_id, arm):
        self.__set_detail(self.right_arms, slot_id, arm)

    def set_left_leg(self, slot_id, leg):
        self.__set_detail(self.left_legs, slot_id, leg)

    def set_right_leg(self, slot_id, leg):
        self.__set_detail(self.right_legs, slot_id, leg)

    def __set_detail(self, slots, slot_id, detail):
        slot = slots.get(slot_id)
        if slot:
            slot.set_detail(detail)
        else:
            raise SlotDoesntExistsError

    # ===== SWITCH =================
    def switch_left_arm(self, slot_id, arm):
        return self.switch_part(self.left_arms, slot_id, arm)

    def switch_right_arm(self, slot_id, arm):
        return self.switch_part(self.right_arms, slot_id, arm)

    def switch_left_leg(self, slot_id, leg):
        return self.switch_part(self.left_legs, slot_id, leg)

    def switch_right_leg(self, slot_id, leg):
        return self.switch_part(self.right_legs, slot_id, leg)

    def switch_part(self, slots, slot_id, detail):
        slot = slots.get(slot_id)
        if slot:
            return slot.switch_detail(detail)
        else:
            raise SlotDoesntExistsError

    @property
    def skills(self):
        return self._skills