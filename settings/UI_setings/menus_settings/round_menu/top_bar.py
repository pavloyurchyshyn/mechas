from settings.screen import SCREEN_W, SCREEN_H, X_SCALE
from visual.UIController import UI_TREE
from constants.UI_names import RoundUINames, RoundButtonsId

X_POS = 0
Y_POS = 0
SIZE_X = SCREEN_W
SIZE_Y = SCREEN_H * 0.025 + 1


def activate_exit_buttons():
    UI_TREE.get_menu(RoundUINames.ExitPopUp).switch()


EXIT_BUTTON = {
    'x': SCREEN_W - 50 * X_SCALE,
    'y': 0,
    'size_x': 50 * X_SCALE,
    'size_y': SIZE_Y,
    'text': 'x',
    'on_click_action': activate_exit_buttons,
}
