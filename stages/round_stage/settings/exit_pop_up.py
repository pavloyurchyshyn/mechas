from settings.screen import SCREEN_W, SCREEN_H
from common.stages import Stages
from visual.UIController import UI_TREE
from stages.round_stage.settings.UI_names import RoundUINames, RoundButtonsId
from visual.font_loader import custom_font
from settings.localization import LocalizationLoader


local = LocalizationLoader().text
stage_controller = Stages()

POP_X_SIZE = 500
POP_Y_SIZE = 200

X_POS = SCREEN_W / 2 - POP_X_SIZE / 2
Y_POS = SCREEN_H / 2 - POP_Y_SIZE / 2

DES_BUTT_SIZE_X = 120
DES_BUTT_SIZE_Y = 120

step_from_border = (POP_X_SIZE - DES_BUTT_SIZE_X - DES_BUTT_SIZE_X) / 3

yes_x_pos = X_POS + step_from_border
no_x_pos = X_POS + POP_X_SIZE - step_from_border - DES_BUTT_SIZE_X

des_y_pos = Y_POS + (POP_Y_SIZE / 2)

EXIT_MESSAGE_SURF = custom_font(25).render(local.UI.round.exit_pop_up.exit_pop_text, 1, (255, 255, 255))


def no_button():
    UI_TREE.get_menu(RoundUINames.ExitPopUp).deactivate()


def yes_button():
    UI_TREE.get_menu(RoundUINames.ExitPopUp).deactivate()
    stage_controller.set_close_round_stage()


EXIT_YES = {
    'x': yes_x_pos,
    'y': des_y_pos,
    'x_size': DES_BUTT_SIZE_X,
    'y_size': DES_BUTT_SIZE_Y,
    'text': local.common.yes,
    'on_click_action': yes_button,
    'id': RoundButtonsId.EXIT_YES,
    'border_parameters': {
        'border_radius': 5,
    },
}

EXIT_NO = {
    'x': no_x_pos,
    'y': des_y_pos,
    'x_size': DES_BUTT_SIZE_X,
    'y_size': DES_BUTT_SIZE_Y,
    'text': local.common.no,
    'on_click_action': no_button,
    'id': RoundButtonsId.EXIT_NO,
    'border_parameters': {
        'border_radius': 5,
    },
}
