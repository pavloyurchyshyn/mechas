from stages.play_stage.round_stage.windows.bars_windows.hp_and_mana_bars import HPBar, ManaBar
from mechas.base.mech import BaseMech


class BarsLogic:
    def __init__(self, mech: BaseMech):
        self.mach: BaseMech = mech

        self.hp_bar = HPBar(mech.full_health_points)
        self.hp_bar.change_hp_regen(mech.health_regen)

        self.mana_bar = ManaBar(mech.full_energy)
        self.mana_bar.change_mana_regen(mech.energy_regen)
        self.mana_bar.change_current_mana(mech.energy)

    def draw(self):
        self.hp_bar.draw()
        self.mana_bar.draw()
