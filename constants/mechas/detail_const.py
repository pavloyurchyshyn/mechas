class MaterialTypes:
    """
    Material types constants.
    """
    METAL_TYPE = 'metal'
    ELECTRIC_TYPE = 'electric'
    STEAM_TYPE = 'steam'
    BIO_TYPE = 'bio'


class DetailsAttrs:
    Id: str = 'unique_id'
    Damage: str = 'damage'
    Armor: str = 'armor'
    AddHP: str = 'add_hp'
    HPRegen: str = 'hp_regen'  # regeneration
    AddEnergy: str = 'add_energy'
    EnergyRegen: str = 'energy_regen'
    Skills: str = 'skills'


class SpecialValues:
    NoCD = 'NoCD'
    NoEnergy = 'NoEnrg'


class MechAttrs:
    Position = 'position'
    BodyClass = 'body_class'
    BodyData = 'body_data'

    LeftArms = 'left_arms'
    RightArms = 'right_arms'
    LeftLegs = 'left_legs'
    RightLegs = 'right_legs'


class BodyInitAttrs:
    unique_id = DetailsAttrs.Id
    arm_class = 'arm_slot_class'
    leg_class = 'leg_slot_class'

    LeftArmsNum = 'left_arms_num'
    RightArmsNum = 'right_arms_num'
    LeftLegsNum = 'left_legs_num'
    RightLegsNum = 'right_legs_num'


class DetailsTypes:
    """
    Details types constants.
    """
    BODY = 'body'
    MOD_TYPE = 'mod'
    WEAPON_TYPE = 'weapon'
    BODY_MOD_TYPE = 'body_mod'
    ARM_AND_LEG_TYPE = 'arm_and_leg'
    ARM_TYPE = 'arm'
    LEG_TYPE = 'leg'


class SlotNames:
    Arm = 'arm_slot'
    Leg = 'leg_slot'
    Weapon = 'weapon_slot'


class MechSerializeConst:
    Body: str = 'body'
    LeftArms: str = 'left_arms'
    RightArms: str = 'right_arms'
    LeftLegs: str = 'left_legs'
    RightLegs: str = 'right_legs'
    Weapon: str = 'weapon'
    Detail: str = 'detail'