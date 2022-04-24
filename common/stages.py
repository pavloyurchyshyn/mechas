from common.singletone import Singleton
from constants.game_stages import *
from common.logger import Logger

LOGGER = Logger().LOGGER


class Stages(metaclass=Singleton):
    def __init__(self):
        self.current_stage = 'main_menu'
        self.set_load_round_stage()


    def get_current_stage(self) -> str:
        return self.current_stage

    def change_current_stage(self, stage: str):
        LOGGER.info(f'Stage {self.current_stage} changed to {stage}')
        self.current_stage = stage

    def set_main_menu_stage(self):
        self.change_current_stage(MAIN_MENU_STAGE)

    def set_main_menu_settings_stage(self):
        self.change_current_stage(MAIN_MENU_SETTINGS_STAGE)

    def set_load_round_stage(self):
        self.change_current_stage(LOADING_STAGE)

    def set_round_stage(self):
        self.change_current_stage(ROUND_STAGE)

    def current_stage_is_menu(self):
        return self.current_stage in MENUS_STAGES_LISTS

    def set_exit_stage(self):
        self.change_current_stage(EXIT_STAGE)
