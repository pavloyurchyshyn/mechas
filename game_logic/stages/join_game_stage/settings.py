from common.stages import Stages
from settings.screen import X_SCALE, Y_SCALE, SCREEN_W, scaled_w, scaled_h
from constants.stages.ids_const import ElementsIDsConst
from constants.stages.localizations.join_menu import JoinMenuLocPaths

JOIN_BUTTONS_DATA = {}
JOIN_BUTTONS_DATA['_exit'] = {
    'kwargs': {
        'size_x': 25 * X_SCALE,
        'size_y': 25 * X_SCALE,
        'x': SCREEN_W - 30 * X_SCALE,
        'y': 10 * Y_SCALE,
        'text': 'X',
        'on_click_action': Stages().set_main_menu_stage,
        'id': ElementsIDsConst.Join.EXIT,
        'border_width': 1,
    }
}

JOIN_BUTTONS_DATA['join'] = {
    'kwargs': {
        'size_x': 100 * X_SCALE,
        'size_y': 50 * Y_SCALE,
        'x': scaled_w(0.945),
        'y': scaled_h(0.95),
        'text': JoinMenuLocPaths.Join,
        'id': ElementsIDsConst.Host.HOST,
        'on_click_action': Stages().set_host_stage,
    }
}
