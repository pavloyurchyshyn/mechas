from constants.mechas.detail_const import *
from mechas.base.exceptions import *
from common.logger import Logger

__all__ = ['BaseDetail', ]


class BaseDetail:
    logger = Logger()

    name = None

    is_limb = False
    is_weapon = False
    material = MaterialTypes.METAL_TYPE
    detail_type = None

    def __init__(self, unique_id=None, **kwargs):
        self.__unique_id = unique_id
        if self.name is None:
            raise NoName(self)

        if self.__unique_id is None:
            raise NotUniqueId(self)

        self._damage = kwargs.get(DetailsAttrs.Damage, 0)
        self._armor = kwargs.get(DetailsAttrs.Armor, 0)
        self._add_hp = kwargs.get(DetailsAttrs.AddHP, 0)
        self._hp_regen = kwargs.get(DetailsAttrs.HPRegen, 0)
        self._add_energy = kwargs.get(DetailsAttrs.AddEnergy, 0)
        self._energy_regen = kwargs.get(DetailsAttrs.EnergyRegen, 0)

        self._skills = kwargs.get(DetailsAttrs.Skills, [])

    @property
    def damage(self):  # name according to DetailAttrs constants
        return self._damage

    @property
    def armor(self):  # name according to DetailAttrs constants
        return self._armor

    @property
    def add_hp(self):  # name according to DetailAttrs constants
        return self._add_hp

    @property
    def hp_regen(self):  # name according to DetailAttrs constants
        return self._hp_regen

    @property
    def add_energy(self):  # name according to DetailAttrs constants
        return self._add_energy

    @property
    def energy_regen(self):  # name according to DetailAttrs constants
        return self._energy_regen

    @property
    def unique_id(self):
        return self.__unique_id

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

    @property
    def skills(self):
        return self._skills