from visual.UI_base.input_element_UI import InputElement
from stages.ids_const import ElementsIDsConst
from settings.screen import scaled_h, scaled_w
from visual.UI_base.localization_mixin import LocalizationMixin

NICKNAME_input = InputElement(x=scaled_w(0.80), y=scaled_h(0.1), max_letters_num=20,
                              id=ElementsIDsConst.MenuSettings.NICKNAME_INPUT)

TEXT_OBJ = {ElementsIDsConst.MenuSettings.NICKNAME_INP_TEXT: {
    'kwargs': {
        'x': scaled_w(0.75),
        'y': scaled_h(0.1),
        'text': '11'  # LocalizationMixin.build_path()
    }
}
}
