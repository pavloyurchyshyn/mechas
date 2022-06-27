from visual.UI_base.localization_mixin import LocalizationMixin


class HostMenuLocPaths:
    loc_path_builder = LocalizationMixin.build_path

    @staticmethod
    def path_in_menu(*args):
        return LocalizationMixin.build_path('UI', 'host_menu', *args)

    Host = path_in_menu('host')