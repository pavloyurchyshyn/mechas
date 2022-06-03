from settings.screen import SCREEN_W, SCREEN_H, HALF_SCREEN_W, X_SCALE, Y_SCALE, GAME_SCALE
from visual.main_window import MAIN_SCREEN
from constants.colors import WHITE, GREY_DARK_2
from settings.global_parameters import set_fps

from common.sound_loader import GLOBAL_MUSIC_PLAYER
from common.stages import Stages
from common.global_keyboard import GLOBAL_KEYBOARD

from visual.UI_buttons.music_volume_progress_bar import VOLUME_PROGRESS_BAR
from visual.UI_buttons.mute_music_button import MUTE_MUSIC_BUTTON
from visual.UI_base.button_UI import Button
from visual.UI_base.text_UI import Text
from visual.UI_base.input_element_UI import InputElement
from visual.UIController import UI_TREE

MAIN_MENU_SETTINGS_BUTTONS = {}

SOUND_ADD_ID = 'sound_add'
SOUND_MINUS_ID = 'sound_minus'
EXIT_ID = 'exit'
RELOAD_COLOR_ID = 'change_color'

KEYBOARD_TEXT_DATA = {}
KEYBOARD_TEXT_OBJS = []
INPUT_ELEMENTS = []


# ------- SOUND SETTINGS --------------

def minus_music_volume():
    GLOBAL_MUSIC_PLAYER.minus_volume()
    VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                               bar_color=WHITE if not GLOBAL_MUSIC_PLAYER.muted else GREY_DARK_2)


def add_music_volume():
    GLOBAL_MUSIC_PLAYER.add_volume()
    VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                               bar_color=WHITE)
    MUTE_MUSIC_BUTTON.change_picture(active=1)


MUSIC_VOLUME_VALUE = Text(p_x_pos=0.01, p_y_pos=0.01,
                          text=f'Music Volume:',
                          screen=MAIN_SCREEN)

KEYBOARD_TEXT_DATA['_FPS'] = {'kwargs': {
    'size': (50, 50),
    'x': 50 * X_SCALE,
    'y': 150 * Y_SCALE,
    'text': 'FPS: ',
    'font_size': 25,
}}

SOUND_BUTTONS = {
    '_sound_minus': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 250 * X_SCALE,
            'y': 100 * Y_SCALE,
            'text': '-',
            'on_click_action': minus_music_volume,
            'id': SOUND_ADD_ID,
            'border_width': 1,
        }
    },

    '_sound_add': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 550 * X_SCALE,
            'y': 100 * Y_SCALE,
            'text': '+',
            'on_click_action': add_music_volume,
            'id': SOUND_MINUS_ID,
            'border_width': 1,

        }
    },

    '_exit': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
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
            'size_x': 40,
            'size_y': 40,
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
            'size_x': 40,
            'size_y': 40,
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
            'size_x': 100,
            'size_y': 40,
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
