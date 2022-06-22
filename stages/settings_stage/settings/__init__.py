from common.stages import Stages
from settings.screen import SCREEN_H, X_SCALE, Y_SCALE, SCREEN_W
from stages.ids_const import ElementsIDsConst

from stages.settings_stage.settings.sound_controll import *
from stages.settings_stage.settings.nickname import NICKNAME_input

MAIN_MENU_SETTINGS_BUTTONS_DATA = {}
MAIN_MENU_SETTINGS_TEXTS_DATA = {}

MAIN_MENU_SETTINGS_BUTTONS_DATA.update(MUSIC_BUTTONS_DATA)
MAIN_MENU_SETTINGS_TEXTS_DATA.update(MUSIC_TEXTS_DATA)

MAIN_MENU_SETTINGS_BUTTONS_DATA['_exit'] = {
    'kwargs': {
        'size_x': 25 * X_SCALE,
        'size_y': 25 * X_SCALE,
        'x': SCREEN_W - 30 * X_SCALE,
        'y': 10 * Y_SCALE,
        'text': 'X',
        'on_click_action': Stages().set_main_menu_stage,
        'id': ElementsIDsConst.MenuSettings.EXIT,
        'border_width': 1,

    }
}
