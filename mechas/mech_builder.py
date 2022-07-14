from game_logic.components.pools.details_pool import DetailsPool
from mechas.base.mech import BaseMech
from mechas.base.parts.body import BaseBody
from constants.mechas.detail_const import MechSerializeConst, DetailsTypes
from common.logger import Logger


class MechBuilder:
    logger = Logger()

    def __init__(self, details_pool: DetailsPool):
        self.details_pool: DetailsPool = details_pool

    def mech_to_dict(self, mech: BaseMech):
        data = {
            MechSerializeConst.Body: mech.body.unique_id,
        }
        for k, slots in ((MechSerializeConst.LeftArms, mech.left_arms),
                         (MechSerializeConst.RightArms, mech.right_arms),
                         (MechSerializeConst.LeftLegs, mech.left_legs),
                         (MechSerializeConst.RightLegs, mech.right_legs)):

            slots = {slot.num: slot.detail for slot in slots.values()}
            for slot_n, detail in slots.items():
                if detail:
                    slots[slot_n] = {MechSerializeConst.Detail: detail.unique_id}
                    if detail.detail_type in (DetailsTypes.ARM_TYPE, DetailsTypes.ARM_AND_LEG_TYPE):
                        if detail.weapon:
                            slots[slot_n][MechSerializeConst.Weapon] = detail.weapon.unique_id

            data[k] = slots

        return data

    def dict_to_body(self, data: dict) -> BaseBody:
        """
        Dict with data in string format about details
        :param data:
        :return:
        """
        body: BaseBody = self.details_pool.get_detail_by_id(data.get(MechSerializeConst.Body))
        for k, set_slot_detail_func in ((MechSerializeConst.LeftArms, body.set_left_arm),
                                        (MechSerializeConst.RightArms, body.set_right_arm),
                                        (MechSerializeConst.LeftLegs, body.set_left_leg),
                                        (MechSerializeConst.RightLegs, body.set_right_leg)):
            side_slots = data.get(k, {})
            for slot_num, detail_data in side_slots.items():
                detail = self.details_pool.get_detail_by_id(detail_data[MechSerializeConst.Detail])
                set_slot_detail_func(slot_num, detail)
                if detail.detail_type in (DetailsTypes.ARM_TYPE, DetailsTypes.ARM_AND_LEG_TYPE):
                    if detail_data.get(MechSerializeConst.Weapon):
                        detail.set_weapon(self.details_pool.get_detail_by_id(detail_data.get(MechSerializeConst.Weapon)))
                    else:
                        detail.remove_weapon()

        return body


if __name__ == '__main__':
    from mechas.default_mech import MetalMech
    from game_logic.components.pools.skills_pool import SkillsPool
    builder = MechBuilder(DetailsPool(SkillsPool()))
    builder.details_pool.load_details_list([
        ('simple_metal_body', '0'),
        ('simple_metal_arm', '1'),
        ('simple_metal_arm', '2'),
        ('simple_metal_leg', '3'),
        ('simple_metal_leg', '4'),
    ])
    m = MetalMech((1, 1))
    print('mech', m.__dict__)
    d = builder.mech_to_dict(m)
    m1 = builder.dict_to_body(d)

    print()
    print(d)
    print(m1.__dict__)
    print(m.body.__dict__)
