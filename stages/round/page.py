from stages.round.UI import RoundUI
from stages.round.windows.arena_window import ArenaWindow
from common.global_mouse import GLOBAL_MOUSE
from pygame.draw import circle as draw_circle
from mechas.base.details import *

base_left_arm = BaseArm(damage=1, armor=2, unique_id=2)
base_right_arm = BaseArm(damage=1, armor=2, unique_id=3)

base_left_leg = BaseLeg(damage=1, armor=2, unique_id=2)
base_right_leg = BaseLeg(damage=1, armor=2, unique_id=3)

mech = BaseMech(left_arms=[base_left_arm, ], right_arms=[base_right_arm, ],
                left_legs=[base_left_leg, ], right_legs=[base_right_leg, ],
                unique_id=1,
                )
from visual.main_window import MAIN_SCREEN


class Round:
    def __init__(self):
        self._arena_window = ArenaWindow()

        self._round_ui = RoundUI()

    def update(self):
        self._round_ui.update()
        self._arena_window.update()
        if GLOBAL_MOUSE.lmb:
            mech.move_into(self._arena_window._current_hex)

    def draw(self):
        self._arena_window.draw()

        self._round_ui.draw()

        if mech._position:
            draw_circle(MAIN_SCREEN, (0, 0, 255), mech._position._center, 5)
            # draw_circle(MAIN_SCREEN, (0, 0, 255), self._arena_window._current_hex._center, 5)


ROUND_STAGE_LOGIC = Round()
