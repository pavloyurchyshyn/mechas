from stages.settings.settings.sound_controll import *

MAIN_MENU_SETTINGS_BUTTONS_DATA = {}
MAIN_MENU_SETTINGS_TEXTS_DATA = {}

MAIN_MENU_SETTINGS_BUTTONS_DATA.update(MUSIC_BUTTONS_DATA)
MAIN_MENU_SETTINGS_TEXTS_DATA.update(MUSIC_TEXTS_DATA)
#
# MAIN_MENU_SETTINGS_BUTTONS_DATA['_exit'] = {
#                                                'kwargs': {
#                                                    'size_x': elements_size,
#                                                    'size_y': elements_size,
#                                                    'x': SCREEN_W - 55 * X_SCALE,
#                                                    'y': 10 * Y_SCALE,
#                                                    'text': 'X',
#                                                    'on_click_action': Stages().set_main_menu_stage,
#                                                    'id': EXIT_ID,
#                                                    'border_width': 1,
#
#                                                }
#                                            },
