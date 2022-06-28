from mechas.base.parts.body import BaseBody
from mechas.base.exceptions import NotEnoughEnergyError
from constants.mechas.detail_const import DetailsAttrs, MechAttrs


class BaseMech:
    """
    This is an object which contains body and calculating attrs.
    Body contains other details.
    """

    def __init__(self, position, body_class=BaseBody, body_data: dict = {}):
        self.body = body_class(**body_data)

        self._position = position

        self._mech_damage = 0
        self._mech_armor = 0
        self._mech_hp = 0
        self._mech_hp_regen = 0
        self._mech_energy = 0
        self._mech_energy_regen = 0

        self._current_hp = 0
        self._current_energy = 0
        self._skills = []
        self.collect_abilities()

    def change_position(self, pos):
        self._position = pos

    def collect_abilities(self):
        self._skills.clear()
        self._skills.extend(self.body.skills)
        ability_names = set()
        for slots in self.parts:
            for slot in slots.values():
                if slot.is_full:
                    for skill in slot.detail.skills:
                        if skill.name not in ability_names:
                            ability_names.add(skill.name)
                            self._skills.extend(slot.detail.skills)

    def calculate_attrs(self):
        print('attrs', self.parts)

        self.calculate_damage()
        self.calculate_armor()
        self.calculate_hp()
        self.calculate_hp_regen()
        self.calculate_energy()
        self.calculate_energy_regen()

    def calculate_damage(self):
        self._mech_damage = self._calculate_parameter(DetailsAttrs.Damage)

    def calculate_armor(self):
        self._mech_armor = self._calculate_parameter(DetailsAttrs.Armor)

    def calculate_hp(self):
        self._mech_hp = self._calculate_parameter(DetailsAttrs.AddHP)

    def calculate_hp_regen(self):
        self._mech_hp_regen = self._calculate_parameter(DetailsAttrs.HPRegen)

    def calculate_energy(self):
        self._mech_energy = self._calculate_parameter(DetailsAttrs.AddEnergy)

    def calculate_energy_regen(self):
        self._mech_energy_regen = self._calculate_parameter(DetailsAttrs.EnergyRegen)

    def _calculate_parameter(self, part_attr):
        v = 0
        for slots in self.parts:
            for slot in slots.values():
                v += getattr(slot.detail, part_attr, 0)

        v += getattr(self.body, part_attr, 0)

        return v

    def deal_damage(self, dmg):
        self._current_hp -= dmg

    def spend_energy(self, energy):
        if energy > self._current_energy:
            raise NotEnoughEnergyError

        self._current_energy -= energy

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def health_points(self):
        return self._current_hp

    @property
    def health_regen(self):
        return self._mech_hp_regen

    @property
    def energy(self):
        return self._current_energy

    @property
    def energy_regen(self):
        return self._mech_energy_regen

    @property
    def damage(self):
        return self._mech_damage

    @property
    def armor(self):
        return self._mech_armor

    @property
    def parts(self):
        return self.left_arms, self.right_arms, self.left_legs, self.right_legs

    @property
    def left_arms(self):
        return self.body.left_arms

    @property
    def right_arms(self):
        return self.body.right_arms

    @property
    def left_legs(self):
        return self.body.left_legs

    @property
    def right_legs(self):
        return self.body.right_legs

    def dict(self):
        return {
            MechAttrs.Damage: self._mech_damage,
            MechAttrs.Armor: self._mech_armor,
            MechAttrs.HP: self._mech_hp,
            MechAttrs.HPRegen: self._mech_hp_regen,
            MechAttrs.Energy: self._mech_energy,
            MechAttrs.EnergyRegen: self._mech_energy_regen,
            MechAttrs.Position: self._position,
        }

    def set_attrs(self, data: dict):
        for key, attr in ((MechAttrs.Damage, '_mech_damage'), (MechAttrs.Armor, '_mech_armor'),
                          (MechAttrs.HP, '_mech_hp'), (MechAttrs.HPRegen, '_mech_hp_regen'),
                          (MechAttrs.Energy, '_mech_energy'), (MechAttrs.EnergyRegen, '_mech_energy_regen'),
                          (MechAttrs.Position, '_position')
                          ):
            setattr(self, attr, data[key] if data.get(key) is not None else getattr(self, attr))

    def __getattr__(self, item):
        return getattr(self.body, item)


if __name__ == '__main__':
    m = BaseMech((0, 0), body_data={'unique_id': 1})
    m.calculate_attrs()
    print(m.dict())
    m.set_attrs(data={MechAttrs.Position: (1, 0)})
    print(m.dict())
