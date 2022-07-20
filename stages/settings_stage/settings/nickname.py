from visual.UI_base.input_element_UI import InputElement
from constants.stages.ids_const import ElementsIDsConst
from settings.screen import scaled_h, scaled_w
from visual.UI_base.localization_mixin import LocalizationMixin

from settings.network import NETWORK_DATA
from common.save_and_load_json_config import get_from_common_config, save_to_common_config
from constants.server.network_keys import PlayerAttrs


def nickname_input(inp: InputElement):
    NETWORK_DATA[PlayerAttrs.Nickname] = inp.text
    save_to_common_config(PlayerAttrs.Nickname, inp.text)


NICKNAME_input = InputElement(x=scaled_w(0.80), y=scaled_h(0.1), max_letters_num=20,
                              text=get_from_common_config(PlayerAttrs.Nickname),
                              on_change_action=nickname_input,
                              id=ElementsIDsConst.MenuSettings.NICKNAME_INPUT)

TEXT_OBJ = {ElementsIDsConst.MenuSettings.NICKNAME_INP_TEXT: {
    'kwargs': {
        'x': scaled_w(0.75),
        'y': scaled_h(0.1),
        'text': LocalizationMixin.build_path('UI', 'main_menu_settings', 'nickname_text'),
    }
}
}
# print('----', TEXT_OBJ)