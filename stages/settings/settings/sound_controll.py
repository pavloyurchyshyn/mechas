from visual.UI_base.progress_bar_UI import ProgressBar
from visual.UIController import UI_TREE
from visual.main_window import MAIN_SCREEN
from common.sound_loader import GLOBAL_MUSIC_PLAYER
from settings.screen import X_SCALE, Y_SCALE
from constants.colors import WHITE, GREY_DARK_2
from constants.game_stages import StagesConstants
from stages.main_menu.settings.menus_settings.ids_const import ElementsIDsConst

__all__ = ['MUSIC_BUTTONS_DATA', 'MUSIC_TEXTS_DATA', 'VOLUME_PROGRESS_BAR']
MUSIC_BUTTONS_DATA = {}
MUSIC_TEXTS_DATA = {}

VOLUME_PROGRESS_BAR = ProgressBar(screen=MAIN_SCREEN,
                                  stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                  stages_num=GLOBAL_MUSIC_PLAYER.volume_stages,
                                  bar_pos=(300 * X_SCALE, 125 * Y_SCALE),
                                  bar_inner_color=GREY_DARK_2 if GLOBAL_MUSIC_PLAYER.muted else WHITE,
                                  bar_x_size=200, bar_y_size=10)


def mute_music_click():
    if GLOBAL_MUSIC_PLAYER.muted:
        GLOBAL_MUSIC_PLAYER.unmute()
        VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                   bar_color=WHITE)
    else:
        GLOBAL_MUSIC_PLAYER.mute()
        VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                   bar_color=GREY_DARK_2)


def minus_music_volume():
    GLOBAL_MUSIC_PLAYER.minus_volume()
    VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                               bar_color=WHITE if not GLOBAL_MUSIC_PLAYER.muted else GREY_DARK_2)


def add_music_volume():
    GLOBAL_MUSIC_PLAYER.add_volume()
    VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                               bar_color=WHITE)
    UI_TREE.get_element(StagesConstants.MAIN_MENU_SETTINGS_STAGE,
                        ElementsIDsConst.MenuSettings.MUTE_MUSIC).change_picture(active=1)


MUSIC_BUTTONS_DATA[ElementsIDsConst.MenuSettings.MUTE_MUSIC] = {
    'kwargs': {
        'x': 600 * X_SCALE,
        'y': 100 * Y_SCALE,
        'size_x': 40,
        'size_y': 40,
        'text': ' ',
        'non_active_text': 'X',
        'on_click_action': mute_music_click,
        'non_active_after_click': 0,
        'change_after_click': 1,
        'border_color': WHITE,
        'border_non_active_color': WHITE,
        'text_non_active_color': WHITE,
        'active_pic': not GLOBAL_MUSIC_PLAYER.muted,
        'screen': MAIN_SCREEN,
        'id': ElementsIDsConst.MenuSettings.MUTE_MUSIC,
        'border_width': 1,
    }
}

MUSIC_BUTTONS_DATA[ElementsIDsConst.MenuSettings.SOUND_MINUS] = {
    'kwargs': {
        'size_x': 40,
        'size_y': 40,
        'p_x_pos': 0.02,
        'p_y_pos': 0.05,
        'text': '-',
        'screen': MAIN_SCREEN,
        'on_click_action': minus_music_volume,
        'id': ElementsIDsConst.MenuSettings.SOUND_MINUS,
        'border_width': 1,
    }
}

MUSIC_BUTTONS_DATA[ElementsIDsConst.MenuSettings.SOUND_ADD] = {
    'kwargs': {
        'size_x': 40,
        'size_y': 40,
        'p_x_pos': 0.04,
        'p_y_pos': 0.05,
        'screen': MAIN_SCREEN,
        'text': '+',
        'on_click_action': add_music_volume,
        'id': ElementsIDsConst.MenuSettings.SOUND_ADD,
        'border_width': 1,
    }
}

# =============================================
MUSIC_TEXTS_DATA[ElementsIDsConst.MenuSettings.MUSIC_VOL_TEXT] = {'p_x_pos': 0.01, 'p_y_pos': 0.05,
                                                                  'text': f'Music Volume:',
                                                                  'screen': MAIN_SCREEN}
