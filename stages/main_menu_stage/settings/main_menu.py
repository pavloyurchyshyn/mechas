from common.stages import Stages
from common.global_clock import ROUND_CLOCK

from settings.screen import HALF_SCREEN_W, GAME_SCALE
from settings.UI_settings.button_settings import ButtonsConst
from settings.localization import LocalizationLoader
from settings.global_parameters import get_language, set_language
from stages.ids_const import ElementsIDsConst
from constants.game_stages import StagesConstants

from visual.UIController import UI_TREE
from visual.main_window import SCREEN_W
from visual.UI_base.disappearing_message import DisappMessage
from visual.UI_base.localization_mixin import LocalizationMixin

STAGES = Stages()
EXIT_WARNING = {'ex_warn': 0}

localization = LocalizationLoader()


def get_menu_loc_path(*path):
    return LocalizationMixin.build_path('UI', 'main_menu', *path)


LANG_BUTTON_ID_PATTERN = 'lang_{}'

on_exit_changes_ids = [ElementsIDsConst.Menu.MENU_START_ID, ElementsIDsConst.Menu.CONNECT_MULTIPLAYER_ID,
                       ElementsIDsConst.Menu.HOST_MULTIPLAYER_ID, ElementsIDsConst.Menu.CHOSEN_LANG_ID,
                       ElementsIDsConst.Menu.MENU_SETTINGS_ID, ElementsIDsConst.Menu.MENU_EXIT_ID]


def choose_lang():
    for l in localization.available_langs:
        el = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, LANG_BUTTON_ID_PATTERN.format(l))
        el.make_visible()
        el.make_active()
    LANG_RELOAD_WARN.activate()


def lang_chosen(lang):
    c = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, ElementsIDsConst.Menu.CHOSEN_LANG_ID)
    c.text = lang
    set_language(lang)
    deactivate_lang_buttons()
    localization.change_language(lang)
    localization.load_current_lang()
    UI_TREE.reload_ui()


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
    STAGES.set_host_stage()
    ROUND_CLOCK.reload()


def activate_exit_warning_message():
    change_exit_warn(1)

    exit_yes = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, ElementsIDsConst.Menu.MENU_EXIT_YES_ID)
    exit_yes.make_active()
    exit_yes.make_visible()

    exit_no = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, ElementsIDsConst.Menu.MENU_EXIT_NO_ID)
    exit_no.make_active()
    exit_no.make_visible()

    for el in on_exit_changes_ids:
        UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, el).make_inactive()

    UI_TREE.drop_focused()
    deactivate_lang_buttons()


def deactivate_exit_warning_message():
    change_exit_warn(0)

    # SURFACE.fill(BLACK)
    exit_yes = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, ElementsIDsConst.Menu.MENU_EXIT_YES_ID)
    exit_yes.make_inactive()
    exit_yes.make_invisible()

    exit_no = UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, ElementsIDsConst.Menu.MENU_EXIT_NO_ID)
    exit_no.make_inactive()
    exit_no.make_invisible()

    for el in on_exit_changes_ids:
        UI_TREE.get_element(StagesConstants.MAIN_MENU_STAGE, el).make_active()

    UI_TREE.drop_focused()


MAIN_MENU_BUTTONS = {
    'start': {
        'kwargs': {
            'x': HALF_SCREEN_W - ButtonsConst.DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.450,
            'active': 1,
            'text': get_menu_loc_path('start_round'),
            'on_click_action': start_game,
            'id': ElementsIDsConst.Menu.MENU_START_ID,
        },
    },
    'host_game_stage': {
        'kwargs': {
            'x': HALF_SCREEN_W - ButtonsConst.DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.510,
            'text': get_menu_loc_path('host_game'),
            # 'active': False,
            # 'on_click_action': STAGES.set_multiplayer_menu_stage,
            'id': ElementsIDsConst.Menu.HOST_MULTIPLAYER_ID,
        }
    },
    'multiplayer': {
        'kwargs': {
            'x': HALF_SCREEN_W - ButtonsConst.DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.570,
            'text': get_menu_loc_path('multiplayer'),
            # 'active': False,
            # 'on_click_action': STAGES.set_multiplayer_menu_stage,
            'id': ElementsIDsConst.Menu.CONNECT_MULTIPLAYER_ID,

        }
    },

    '_settings': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - ButtonsConst.DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.630,
            'text': get_menu_loc_path('settings'),
            'on_click_action': STAGES.set_main_menu_settings_stage,
            'id': ElementsIDsConst.Menu.MENU_SETTINGS_ID,

        }
    },
    '_exit': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - ButtonsConst.DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.690,
            'text': get_menu_loc_path('exit'),
            'id': ElementsIDsConst.Menu.MENU_EXIT_ID,
            'on_click_action': activate_exit_warning_message,
            'border_non_active_color': (255, 255, 255),
            'text_non_active_color': (255, 255, 255)

        }
    },
    '_exit_yes': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - ButtonsConst.DEFAULT_BUTTON_X_SIZE,
            'p_y_pos': 0.5,
            'text': get_menu_loc_path('exit_yes'),
            'active': 0,
            'visible': False,
            'on_click_action': STAGES.set_exit_stage,
            'non_visible_after_click': 1,
            'non_active_after_click': 1,
            'id': ElementsIDsConst.Menu.MENU_EXIT_YES_ID,
            'border_non_active_color': (255, 255, 255),
            'text_non_active_color': (255, 255, 255)
        }
    },

    '_exit_no': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W + ButtonsConst.DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.5,
            'text': get_menu_loc_path('exit_no'),
            'active': 0,
            'visible': False,
            'non_visible_after_click': 1,
            'non_active_after_click': 1,
            'id': ElementsIDsConst.Menu.MENU_EXIT_NO_ID,
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
                                 'id': ElementsIDsConst.Menu.CHOSEN_LANG_ID,
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

LANG_RELOAD_WARN = DisappMessage(text=get_menu_loc_path('lang_disapp_msg'),
                                 id=ElementsIDsConst.Menu.LANG_WARN_MESG,
                                 exists_time=10,
                                 x=int(lang_x - 2 - 200 * GAME_SCALE), y=2,
                                 size_x=int(200 * GAME_SCALE), size_y=int(50 * GAME_SCALE))
