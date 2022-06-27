from visual.UI_base.localization_mixin import LocalizationMixin


class JoinMenuLocPaths:
    loc_path_builder = LocalizationMixin.build_path

    @staticmethod
    def path_in_menu(*args):
        return LocalizationMixin.build_path('UI', 'join_menu', *args)

    Join = path_in_menu('join')