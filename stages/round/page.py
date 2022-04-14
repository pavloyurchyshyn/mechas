from stages.round.UI import RoundUI
from stages.round.windows.arena_window import ArenaWindow


class Round:
    def __init__(self):
        self._arena_window = ArenaWindow()

        self._round_ui = RoundUI()

    def update(self):
        self._round_ui.update()
        self._arena_window.update()

    def draw(self):
        self._arena_window.draw()

        self._round_ui.draw()


ROUND_STAGE_LOGIC = Round()
