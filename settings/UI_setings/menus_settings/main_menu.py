from common.stages import Stages
from common.global_clock import ROUND_CLOCK

from settings.screen import HALF_SCREEN_W, GAME_SCALE
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE
from settings.localization import LocalizationLoader
from settings.global_parameters import get_language, set_language

from constants.game_stages import StagesConstants

from visual.UIController import UI_TREE
from visual.main_window import SCREEN_W
from visual.UI_base.disappearing_message import DisappMessage

STAGES = Stages()
EXIT_WARNING = {'ex_warn': 0}

localization = LocalizationLoader()
menu_text = localization.text.UI.main_menu

LANG_BUTTON_ID_PATTERN = 'lang_{}'
MENU_EXIT_YES_ID = 'menu_exit_yes'
MENU_EXIT_NO_ID = 'menu_exit_no'
MENU_START_ID = 'menu_start'
CONNECT_MULTIPLAYER_ID = 'menu_connect_multiplayer'
HOST_MULTIPLAYER_ID = 'menu_host_multiplayer'
MENU_SETTINGS_ID = 'menu_settings'
MENU_EXIT_ID = 'menu_exit'
CHOSEN_LANG_ID = 'chosen_lang'
LANG_WARN_MESG = 'lang_wan_message'

on_exit_changes_ids = [MENU_START_ID, CONNECT_MULTIPLAYER_ID, HOST_MULTIPLAYER_ID,
                       CHOSEN_LANG_ID, MENU_SETTINGS_ID, MENU_EXIT_ID]


def choose_lang():
    for l in localization.available_langs:
        el = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, LANG_BUTTON_ID_PATTERN.format(l))
        el.make_visible()
        el.make_active()
    LANG_RELOAD_WARN.activate()


def lang_chosen(lang):
    c = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, CHOSEN_LANG_ID)
    c.text = lang
    set_language(lang)
    deactivate_lang_buttons()


def deactivate_lang_buttons():
    for l in localization.available_langs:
        el = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, LANG_BUTTON_ID_PATTERN.format(l))
        el.make_invisible()
        el.make_inactive()


def exit_warning():
    return EXIT_WARNING['ex_warn']


def change_exit_warn(val):
    EXIT_WARNING['ex_warn'] = val


def start_game():
    STAGES.set_load_round_stage()
    ROUND_CLOCK.reload()


def activate_exit_warning_message():
    change_exit_warn(1)

    exit_yes = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, MENU_EXIT_YES_ID)
    exit_yes.make_active()
    exit_yes.make_visible()

    exit_no = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, MENU_EXIT_NO_ID)
    exit_no.make_active()
    exit_no.make_visible()

    for el in on_exit_changes_ids:
        UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, el).make_inactive()

    UI_TREE.drop_focused()
    deactivate_lang_buttons()


def deactivate_exit_warning_message():
    change_exit_warn(0)

    # SURFACE.fill(BLACK)
    exit_yes = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, MENU_EXIT_YES_ID)
    exit_yes.make_inactive()
    exit_yes.make_invisible()

    exit_no = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, MENU_EXIT_NO_ID)
    exit_no.make_inactive()
    exit_no.make_invisible()

    for el in on_exit_changes_ids:
        UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, el).make_active()

    UI_TREE.drop_focused()


MAIN_MENU_BUTTONS = {
    'start': {
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.450,
            'active': 1,
            'text': menu_text.start_round,
            'on_click_action': start_game,
            'id': MENU_START_ID,
        },
    },
    'host_game': {
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.510,
            'text': menu_text.host_game,
            # 'active': False,
            # 'on_click_action': STAGES.set_multiplayer_menu_stage,
            'id': HOST_MULTIPLAYER_ID,
        }
    },
    'multiplayer': {
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.570,
            'text': menu_text.multiplayer,
            # 'active': False,
            # 'on_click_action': STAGES.set_multiplayer_menu_stage,
            'id': CONNECT_MULTIPLAYER_ID,

        }
    },

    '_settings': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.630,
            'text': menu_text.settings,
            'on_click_action': STAGES.set_main_menu_settings_stage,
            'id': MENU_SETTINGS_ID,

        }
    },
    '_exit': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.690,
            'text': menu_text.exit,
            'id': MENU_EXIT_ID,
            'on_click_action': activate_exit_warning_message,
            'border_non_active_color': (255, 255, 255),
            'text_non_active_color': (255, 255, 255)

        }
    },
    '_exit_yes': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE,
            'p_y_pos': 0.5,
            'text': menu_text.exit_yes,
            'active': 0,
            'visible': False,
            'on_click_action': STAGES.set_exit_stage,
            'non_visible_after_click': 1,
            'non_active_after_click': 1,
            'id': MENU_EXIT_YES_ID,
            'border_non_active_color': (255, 255, 255),
            'text_non_active_color': (255, 255, 255)
        }
    },

    '_exit_no': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W + DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.5,
            'text': menu_text.exit_no,
            'active': 0,
            'visible': False,
            'non_visible_after_click': 1,
            'non_active_after_click': 1,
            'id': MENU_EXIT_NO_ID,
            'border_non_active_color': (255, 255, 255),
            'text_non_active_color': (255, 255, 255),
            'on_click_action': deactivate_exit_warning_message
        }
    },

}

lang_size = 50 * GAME_SCALE

lang_x = SCREEN_W - lang_size - 2
lang_y = 2

MAIN_MENU_BUTTONS['lang'] = {'args': (),
                             'kwargs': {
                                 'x': lang_x,
                                 'y': lang_y,
                                 'size_x': lang_size,
                                 'text': get_language().upper(),
                                 'on_click_action': choose_lang,
                                 'id': CHOSEN_LANG_ID,
                             }
                             }
lang_y += 5
for lang in localization.available_langs:
    lang_y += 2 + lang_size

    MAIN_MENU_BUTTONS[lang.upper()] = {
        'args': (),
        'kwargs': {
            'x': lang_x,
            'y': lang_y,
            'size_x': lang_size,
            'text': lang.upper(),
            'active': 0,
            'visible': False,
            'id': LANG_BUTTON_ID_PATTERN.format(lang),
            'on_click_action_args': (lang.upper(),),
            'on_click_action': lang_chosen,
        }
    }

LANG_RELOAD_WARN = DisappMessage(text=menu_text.lang_disapp_msg, id=LANG_WARN_MESG,
                                 exists_time=10,
                                 x=int(lang_x - 2 - 200 * GAME_SCALE), y=2,
                                 size_x=int(200 * GAME_SCALE), size_y=int(50 * GAME_SCALE))
