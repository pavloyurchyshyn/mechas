from common.singleton import Singleton
from constants.game_stages import StagesConstants
from common.logger import Logger

LOGGER = Logger()


class Stages(metaclass=Singleton):
    def __init__(self):
        self.current_stage = 'main_menu_stage'
        # self.set_load_round_stage()
        # self.set_main_menu_settings_stage()

    def get_current_stage(self) -> str:
        return self.current_stage

    def change_current_stage(self, stage: str):
        LOGGER.info(f'Stage {self.current_stage} changed to {stage}')
        self.current_stage = stage

    def set_host_stage(self):
        self.change_current_stage(StagesConstants.HOST)

    def set_connect_stage(self):
        self.change_current_stage(StagesConstants.CONNECT)

    def set_main_menu_stage(self):
        self.change_current_stage(StagesConstants.MAIN_MENU_STAGE)

    def set_main_menu_settings_stage(self):
        self.change_current_stage(StagesConstants.MAIN_MENU_SETTINGS_STAGE)

    # def set_load_round_stage(self):
    #     self.change_current_stage(StagesConstants.LOADING_STAGE)

    def set_round_stage(self):
        self.change_current_stage(StagesConstants.ROUND_STAGE)

    def set_close_round_stage(self):
        self.change_current_stage(StagesConstants.ROUND_CLOSE)

    def current_stage_is_menu(self):
        return self.current_stage in StagesConstants.MENUS_STAGES_LISTS

    def set_exit_stage(self):
        self.change_current_stage(StagesConstants.EXIT_STAGE)
