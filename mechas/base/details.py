from constants.mechas.detail_const import *
from mechas.base.exceptions import *
from common.logger import Logger


class BaseDetail:
    logger = Logger().LOGGER

    name = None

    is_limb = False
    material = MaterialTypes.METAL_TYPE
    detail_type = None

    def __init__(self, unique_id=None, damage=0, armor=0):
        self.__unique_id = unique_id
        if self.__unique_id is None:
            raise NotUniqueId(self)

        self._damage = damage
        self._armor = armor

    @property
    def unique_id(self):
        return self.__unique_id

    @property
    def damage(self):
        return self._damage

    @property
    def armor(self):
        return self._armor

    @property
    def is_arm(self) -> bool:
        return self.detail_type in (DetailsTypes.ARM_TYPE, DetailsTypes.ARM_AND_LEG_TYPE)

    @property
    def is_leg(self) -> bool:
        return self.detail_type in (DetailsTypes.LEG_TYPE, DetailsTypes.ARM_AND_LEG_TYPE)

    @property
    def is_mod(self) -> bool:
        return self.detail_type in (DetailsTypes.MOD_TYPE, DetailsTypes.BODY_MOD_TYPE)

    @property
    def is_body(self) -> bool:
        return self.detail_type in (DetailsTypes.BODY,)

    @property
    def is_body_mod(self) -> bool:
        return self.detail_type is DetailsTypes.BODY_MOD_TYPE


class ModificationsSlots:
    def __init__(self, mods_num=0, mods_dict: dict = None, acceptable_mods_types=None):
        self._mods_num = mods_num
        self._acceptable_mods_types = acceptable_mods_types
        self.__mods_slots = mods_dict if mods_dict else {i + 1: None for i in range(self._mods_num)}

    def add_mod(self, mod):
        if all(self.__mods_slots.values()):
            raise NoSlotsForMods(self)
        else:
            for k, v in self.__mods_slots.items():
                if v is None:
                    self.__mods_slots[k] = mod

    def remove_mod(self, mod):
        for k, m in self.__mods_slots.items():
            if m == mod:
                self.__mods_slots[k] = None

    def clear_mods(self):
        self.__mods_slots.clear()
        for i in range(self._mods_num):
            self.__mods_slots[i + 1] = None

    @property
    def mods(self):
        return self.__mods_slots


class BaseLimb(BaseDetail, ModificationsSlots):
    is_limb = True

    def __init__(self, mods_num=0, mods_dict={}, *args, **kwargs):
        super().__init__(*args, *kwargs)
        ModificationsSlots.__init__(self, mods_num, mods_dict)


class BaseArm(BaseLimb):
    detail_type = DetailsTypes.ARM_TYPE

    def __init__(self, weapon_able=False, weapon=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._weapon_able = weapon_able
        self._weapon_slot = weapon if weapon_able else None

    def set_weapon(self, weapon):
        if self._weapon_able:
            self._weapon_slot = weapon

    def remove_weapon(self):
        self._weapon_slot = None

    @property
    def weapon(self):
        return self._weapon_slot


class BaseLeg(BaseLimb):
    is_limb = True
    detail_type = DetailsTypes.LEG_TYPE

    def __init__(self, steps=1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._steps = steps


class BaseBody(BaseDetail, ModificationsSlots):
    detail_type = DetailsTypes.BODY

    class Sides:
        LEFT = 'left'
        RIGHT = 'right'

    def __init__(self, left_arms_count=1, right_arms_count=1,
                 left_legs_count=1, right_legs_count=1,
                 mods_num=0, mods_dict={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ModificationsSlots.__init__(self, mods_num, mods_dict)

        self._left_arm_count = left_arms_count
        self._right_arm_count = right_arms_count
        self._left_leg_count = left_legs_count
        self._right_leg_count = right_legs_count

        self._left_arm_slots = {}
        self._right_arm_slots = {}
        self._left_leg_slots = {}
        self._right_leg_slots = {}

    # def add_arm(self, arm):
    #     if not arm.is_arm:
    #         raise WrongDetailType
    #
    #     if len(self._right_arm_slots) >= self._right_arm_count and len(self._left_arm_slots) >= self._left_arm_count:
    #         raise NoSlotsForArms(self)
    #
    #     left_arm_count = len(self._left_arm_slots)
    #     right_arm_count = len(self._right_arm_slots)
    #     # if have free slots and num less than in right side
    #     if left_arm_count < self._left_arm_count and left_arm_count <= right_arm_count:
    #         self.add_left_arm(arm)
    #     else:
    #         self.add_right_arm(arm)

    def add_left_arm(self, arm):
        self.__add_arm_to_side(self._left_arm_slots, arm, self._left_arm_count)

    def add_right_arm(self, arm):
        self.__add_arm_to_side(self._right_arm_slots, arm, self._right_arm_count)

    def __add_arm_to_side(self, side_slots, arm: BaseArm, side_count):
        if not arm.is_arm:
            raise WrongDetailType(arm, DetailsTypes.ARM_TYPE)

        self.__add_detail_to_slots(side_slots, arm, side_count)

    def add_left_leg(self, leg):
        self.__add_leg_to_side(self._left_leg_slots, leg, self._left_leg_count)

    def add_right_leg(self, leg):
        self.__add_leg_to_side(self._right_leg_slots, leg, self._right_leg_count)

    def __add_leg_to_side(self, side_slots, leg: BaseLeg, side_count):
        if not leg.is_leg:
            raise WrongDetailType

        self.__add_detail_to_slots(side_slots, leg, side_count)

    def __add_detail_to_slots(self, side_slots, detail, side_count):
        if len(side_slots) == side_count:
            raise NoSlotsForLimbs(self)

        if detail.unique_id in side_slots:
            raise DetailAlreadyConnected(self, detail)

        side_slots[detail.unique_id] = detail

    def add_arms(self, arms: dict):
        for side, arms_ in arms.items():
            add_arm = self.add_left_arm if side == self.Sides.LEFT else self.add_right_arm
            self.__add_details(add_arm, arms_)

    def add_legs(self, legs: dict):
        for side, legs_ in legs.items():
            add_leg = self.add_left_leg if side == self.Sides.LEFT else self.add_right_leg
            self.__add_details(add_leg, legs_)

    def __add_details(self, add_func, details):
        for detail in details:
            try:
                add_func(detail)
            except Exception as e:
                self.logger.error(e)


class BaseMech(BaseBody):

    def __init__(self, left_arms_count=1, right_arms_count=1,
                 left_legs_count=1, right_legs_count=1,
                 mods_num=0, mods_dict={},
                 left_arms=[], right_arms=[],
                 left_legs=[], right_legs=[],
                 *args, **kwargs):
        super().__init__(left_arms_count, right_arms_count, left_legs_count, right_legs_count,
                         mods_num, mods_dict, *args, **kwargs)

        self.add_arms({BaseBody.Sides.LEFT: left_arms, BaseBody.Sides.RIGHT: right_arms})
        self.add_legs({BaseBody.Sides.LEFT: left_legs, BaseBody.Sides.RIGHT: right_legs})

        self._position = None

    def move_into(self, new_hex):
        self._position = new_hex
    # def build(self):



