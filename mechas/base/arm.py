from mechas.base.detail import BaseDetail
from mechas.base.slot import BaseSlot
from constants.mechas.detail_const import *


class BaseArm(BaseDetail):
    is_limb = True
    detail_type = DetailsTypes.ARM_TYPE
    can_handle_weapon = True

    def __init__(self, unique_id, weapon=None, **kwargs):
        super().__init__(unique_id=unique_id, **kwargs)
        self.__weapon = BaseSlot(weapon, 0) if self.can_handle_weapon else None

    def set_weapon(self, weapon):
        self.__weapon.set_detail(weapon)

    def remove_weapon(self):
        return self.__weapon.get_and_clear()

    @property
    def weapon(self):
        if self.__weapon:
            return self.__weapon.detail
        else:
            return None
