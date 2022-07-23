from game_logic.components.pools.details_pool import DetailsPool
from mechas.base.mech import BaseMech
from mechas.base.parts.body import BaseBody
from constants.mechas.detail_const import MechSerializeConst, DetailsTypes, MechAttrs
from common.logger import Logger


class MechBuilder:
    logger = Logger()

    def __init__(self, details_pool: DetailsPool):
        self.details_pool: DetailsPool = details_pool

    def mech_to_dict(self, mech: BaseMech):
        data = {
            MechSerializeConst.Body: mech.body.unique_id,
            MechAttrs.Position: mech.position,
            MechAttrs.CurrentHP: mech.health_points,
            MechAttrs.CurrentEnergy: mech.energy,
        }
        for key, slots in (
                (MechSerializeConst.LeftSlots, mech.left_slots),
                (MechSerializeConst.RightSlots, mech.right_slots),
        ):

            slots = {num: slot.detail for num, slot in slots.items()}
            for slot_n, detail in slots.items():
                if detail:
                    slots[slot_n] = {MechSerializeConst.Detail: detail.unique_id}
                    if detail.detail_type in (DetailsTypes.ARM_TYPE, DetailsTypes.ARM_AND_LEG_TYPE):
                        if detail.weapon:
                            slots[slot_n][MechSerializeConst.Weapon] = detail.weapon.unique_id

            data[key] = slots

        return data

    def dict_to_mech(self, data: dict) -> BaseMech:
        """
        Dict with data in string format about details
        :param data:
        :return:
        """
        body: BaseBody = self.details_pool.get_detail_by_id(data.get(MechSerializeConst.Body))
        print(data.get(MechSerializeConst.Body), self.details_pool.id_to_detail)
        print('build body', body)
        mech = BaseMech(data.get(MechAttrs.Position), body_detail=body)

        for k, set_slot_detail_func in ((MechSerializeConst.LeftSlots, mech.set_left_detail),
                                        (MechSerializeConst.RightSlots, mech.set_right_detail),
                                        ):
            side_slots = data.get(k, {})
            for slot_num, detail_data in side_slots.items():
                detail = self.details_pool.get_detail_by_id(detail_data[MechSerializeConst.Detail])
                set_slot_detail_func(slot_num, detail)
                if detail.detail_type in (DetailsTypes.ARM_TYPE, DetailsTypes.ARM_AND_LEG_TYPE):
                    if detail_data.get(MechSerializeConst.Weapon):
                        detail.set_weapon(
                            self.details_pool.get_detail_by_id(detail_data.get(MechSerializeConst.Weapon)))
                    else:
                        detail.remove_weapon()

        mech.set_energy(data.get(MechAttrs.CurrentEnergy, 0))
        mech.set_health_points(data.get(MechAttrs.CurrentHP, 0))

        return mech


if __name__ == '__main__':
    from mechas.test_mech import MetalMech
    from game_logic.components.pools.skills_pool import SkillsPool

    builder = MechBuilder(DetailsPool(SkillsPool()))
    builder.details_pool.load_details_list([
        ('simple_metal_body', 0),
        ('simple_metal_arm', 1),
        ('simple_metal_arm', 2),
        ('simple_metal_leg', 3),
        ('simple_metal_leg', 4),
    ])
    m = MetalMech((1, 0))
    print('mech', m.__dict__)
    d = builder.mech_to_dict(m)
    print('mech dict', d)
    m1 = builder.dict_to_mech(d)

    print()
    print(d)
    print('# ===================')
    print(m.__dict__)
    print(m1.__dict__)

    print(m.attr_dict(), m.attr_dict() == m1.attr_dict(), m1.attr_dict())
