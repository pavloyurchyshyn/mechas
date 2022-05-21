from visual.UIController import UI_TREE
from constants.UI_names import RoundUINames
from settings.UI_setings.menus_settings.round_menu.windows_sizes import RoundSizes


def activate_exit_buttons():
    UI_TREE.get_menu(RoundUINames.ExitPopUp).switch()


EXIT_BUTTON = {
    'x': RoundSizes.TopBar.EXIT_B_X,
    'y': RoundSizes.TopBar.EXIT_B_Y,
    'size_x': RoundSizes.TopBar.EXIT_B_X_SIZE,
    'size_y': RoundSizes.TopBar.EXIT_B_Y_SIZE,
    'text': 'x',
    'on_click_action': activate_exit_buttons,
}
