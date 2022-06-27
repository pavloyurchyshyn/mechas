from visual.UI_base.localization_mixin import LocalizationMixin


class MainMenuLocPaths:
    loc_path_builder = LocalizationMixin.build_path

    @staticmethod
    def path_in_menu(*args):
        return LocalizationMixin.build_path('UI', 'main_menu', *args)

    StartRound = path_in_menu('menu_start')
    Multiplayer = path_in_menu('multiplayer')
    Settings = path_in_menu('settings')
    Exit = path_in_menu('exit')
    ExitYes = path_in_menu('exit_yes')
    ExitNo = path_in_menu('exit_no')
    HostGame = path_in_menu('host_game')
    LangDisappMsg = path_in_menu('lang_disapp_msg')
