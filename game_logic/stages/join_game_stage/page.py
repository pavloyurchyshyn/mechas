from visual.UI_base.menu_UI import MenuUI
from visual.main_window import MAIN_SCREEN
from constants.game_stages import StagesConstants
from game_logic.stages.join_game_stage.settings import JOIN_BUTTONS_DATA


class JoinWindow(MenuUI):
    def __init__(self):
        super(JoinWindow, self).__init__(
            buttons=JOIN_BUTTONS_DATA,
            name=StagesConstants.HOST,
            surface=MAIN_SCREEN)

        self.create_buttons()
        self.add_elements_to_controller(*self._elements)

    def update(self):
        if self.click():
            xy = self.GLOBAL_MOUSE.pos
            for button in self._buttons:
                button.click(xy=xy)
                if button.clicked:
                    break

    def draw(self, dx=0, dy=0):
        for element in self._elements:
            element.draw(dx, dy)
