from settings.global_parameters import set_fps

from common.stages import Stages

from visual.UI_buttons.music_volume_progress_bar import VOLUME_PROGRESS_BAR
from visual.UI_base.text_UI import Text
from visual.main_window import MAIN_SCREEN

from common.sound_loader import GLOBAL_MUSIC_PLAYER

from settings.screen import X_SCALE, Y_SCALE, SCREEN_W, SCREEN_H, HALF_SCREEN_W, GAME_SCALE

from constants.colors import WHITE, GREY_DARK_2

MAIN_MENU_SETTINGS_BUTTONS = {}

EXIT_ID = 'exit'
RELOAD_COLOR_ID = 'change_color'

KEYBOARD_TEXT_DATA = {}
KEYBOARD_TEXT_OBJS = []
INPUT_ELEMENTS = []

# ------- SOUND SETTINGS --------------


MUSIC_VOLUME_VALUE = Text(p_x_pos=0.01, p_y_pos=0.05,
                          text=f'Music Volume:',
                          screen=MAIN_SCREEN)

elements_size = 30 * X_SCALE
SOUND_BUTTONS = {
    '_FPS': {'kwargs': {
        'size': (50, 50),
        'p_x_pos': 0.01,
        'p_y_pos': 0.05,
        'text': 'FPS: ',
        'font_size': 25,
    }},

    '_exit': {
        'kwargs': {
            'size_x': elements_size,
            'size_y': elements_size,
            'x': SCREEN_W - 55 * X_SCALE,
            'y': 10 * Y_SCALE,
            'text': 'X',
            'on_click_action': Stages().set_main_menu_stage,
            'id': EXIT_ID,
            'border_width': 1,

        }
    },

    '_set_fps_60': {
        'kwargs': {
            'size_x': elements_size,
            'size_y': elements_size,
            'x': 110 * X_SCALE,
            'y': 150 * Y_SCALE,
            'text': '60',
            'on_click_action': set_fps,
            'on_click_action_args': (60,),
            'id': 'fps_60',
            'border_width': 1,

        }
    },

    '_set_fps_120': {
        'kwargs': {
            'size_x': elements_size,
            'size_y': elements_size,
            'x': 160 * X_SCALE,
            'y': 150 * Y_SCALE,
            'text': '120',
            'on_click_action': set_fps,
            'on_click_action_args': (120,),
            'border_width': 1,

            'id': 'fps_120',
        }
    },

    '_set_fps_no_limit': {
        'kwargs': {
            'size_x': elements_size * 3,
            'size_y': elements_size,
            'x': 210 * X_SCALE,
            'y': 150 * Y_SCALE,
            'text': 'No limit',
            'on_click_action': set_fps,
            'on_click_action_args': (0,),
            'id': 'fps_0',
            'border_width': 1,

        }
    },
}
# -------------------------------------------------------------

MAIN_MENU_SETTINGS_BUTTONS.update(SOUND_BUTTONS)

# MAIN_MENU_SETTINGS_BUTTONS.clear()
# KEYBOARD_TEXT_DATA.clear()
# INPUT_ELEMENTS.clear()
# KEYBOARD_TEXT_OBJS.clear()
