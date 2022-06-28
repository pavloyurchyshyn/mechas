from pygame.draw import rect as draw_rect
from obj_properties.rect_form import Rectangle
from game_logic.stages.round_stage.settings.windows_sizes import RoundSizes
from visual.UI_base.text_UI import Text
from visual.UI_base.progress_bar_UI import ProgressBar
from visual.main_window import MAIN_SCREEN
from constants.stages.localizations.round import RoundLocPaths
from settings.localization import LocalizationLoader
from visual.UI_base.localization_mixin import LocalizationMixin

localization = LocalizationLoader()


class ManaBar:

    def __init__(self):
        self.current_mana = ProgressBar(bar_pos=(RoundSizes.Bars.Mana.X, RoundSizes.Bars.Mana.Y),
                                        bar_x_size=RoundSizes.Bars.X_SIZE, bar_y_size=RoundSizes.Bars.Y_SIZE,
                                        border_radius=5, out_border_radius=5,
                                        border_x_step=4, border_y_step=4,
                                        bar_color=(50, 50, 155),
                                        stage=50, stages_num=110
                                        )
        x, y = RoundSizes.Bars.Mana.text_pos
        self.mana_text = LocalizationMixin.get_text_with_localization(RoundLocPaths.ManaText) + ': {}/{}'
        self.mana_text_obj = Text(self.mana_text.format(*self.current_mana.values), raw_text=True, x=x, y=y)

        x, y = RoundSizes.Bars.Mana.reg_text_pos
        self.mana_reg_obj = Text('0', raw_text=True, x=x, y=y)

        self.mana_after_actions = ProgressBar(bar_pos=(RoundSizes.Bars.Mana.X, RoundSizes.Bars.Mana.Y),
                                              bar_x_size=RoundSizes.Bars.X_SIZE, bar_y_size=RoundSizes.Bars.Y_SIZE,
                                              border_radius=5, out_border_radius=5,
                                              border_x_step=4, border_y_step=4,
                                              bar_color=(150, 150, 255),
                                              stage=20, stages_num=110,
                                              border_width=0,
                                              )

    def render(self):
        self.mana_text_obj.change_text(self.mana_text.format(*self.current_mana.values))

    def change_current_mana(self, current_mana):
        self.current_mana.change_current_stage(current_mana)

    def change_current_mana_after_actions(self, current_mana):
        self.mana_after_actions.change_current_stage(current_mana)

    def change_mana_pool(self, mana_pool):
        self.current_mana.change_stages_num(mana_pool)
        self.mana_after_actions.change_stages_num(mana_pool)

    def change_mana_regen(self, regen_val):
        if regen_val >= 0:
            regen_val = f'+{regen_val}'
        else:
            regen_val = f'-{regen_val}'
        self.mana_reg_obj.change_text(regen_val)

    def draw(self):
        self.mana_text_obj.draw()
        self.mana_reg_obj.draw()
        self.current_mana.draw()
        self.mana_after_actions.draw()


class HPBar:
    def __init__(self):
        self.hp_bar = ProgressBar(
            bar_pos=(RoundSizes.Bars.HP.X, RoundSizes.Bars.HP.Y),
            bar_x_size=RoundSizes.Bars.X_SIZE, bar_y_size=RoundSizes.Bars.Y_SIZE,
            border_radius=5, out_border_radius=5,
            border_x_step=4, border_y_step=4,
            bar_color=(50, 155, 50),
            stage=5, stages_num=11
        )

        x, y = RoundSizes.Bars.HP.text_pos
        self.hp_text = LocalizationMixin.get_text_with_localization(RoundLocPaths.HPText) + ': {}/{}'
        self.hp_text_obj = Text(self.hp_text.format(*self.hp_bar.values), raw_text=True, x=x, y=y)

        x, y = RoundSizes.Bars.HP.reg_text_pos
        self.mana_reg_obj = Text('0', raw_text=True, x=x, y=y)

    def draw(self):
        self.hp_bar.draw()
        self.hp_text_obj.draw()
        self.mana_reg_obj.draw()

    def render(self):
        self.hp_text_obj.change_text(self.hp_text.format(*self.hp_bar.values))

    def change_hp_regen(self, regen_val):
        if regen_val >= 0:
            regen_val = f'+{regen_val}'
        else:
            regen_val = f'-{regen_val}'
        self.mana_reg_obj.change_text(regen_val)
