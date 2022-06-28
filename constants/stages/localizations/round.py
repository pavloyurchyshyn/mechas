from visual.UI_base.localization_mixin import LocalizationMixin


class RoundLocPaths:
    loc_path_builder = LocalizationMixin.build_path

    @staticmethod
    def path_in_menu(*args):
        return LocalizationMixin.build_path('UI', 'round', *args)

    ExitPopUp = path_in_menu('exit_pop_up', 'exit_pop_text')
    ExitYes = loc_path_builder('common', 'yes')
    ExitNo = loc_path_builder('common', 'no')

    ReadyButton = 'ready_button'
    ManaText = path_in_menu('mana_text')
    HPText = path_in_menu('hp_text')