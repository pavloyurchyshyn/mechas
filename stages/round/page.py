from stages.round.UI import RoundUI
from stages.round.windows.arena_window import ArenaWindow
from stages.round.windows.top_bar import TopBar
from stages.round.windows.exit_pop_up import ExitPopUp

from visual.UIController import UI_TREE

from common.global_mouse import GLOBAL_MOUSE

from pygame.draw import circle as draw_circle

from visual.main_window import MAIN_SCREEN


class Round:
    def __init__(self):
        self._arena_window = ArenaWindow()
        self._top_bar = TopBar()
        self._exit_pop_up = ExitPopUp()

        self._round_ui = RoundUI()

    def update(self, request_data):
        if self._exit_pop_up.active:
            self._exit_pop_up.update()
        else:
            self._round_ui.update()
            self._arena_window.update()
            self._top_bar.update()

    def draw(self):
        self._arena_window.draw()

        self._round_ui.draw()

        self._top_bar.draw()

        if self._exit_pop_up.active:
            self._exit_pop_up.draw()


ROUND_STAGE_LOGIC = Round()
