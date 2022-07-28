from settings.screen import scaled_w, scaled_h
from settings.screen import GAME_SCALE
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes

SLOT_X_SIZE = scaled_w(0.05)
SLOT_Y_SIZE = scaled_h(0.15)


class SlotSettings:
    MIN_STEP_BETWEEN_SLOTS = 20
    X_SIZE = SLOT_X_SIZE
    Y_SIZE = SLOT_Y_SIZE
    round_value = 5

    class Title:
        Y = scaled_h(0.0012)
        font_size = 10 * GAME_SCALE
        X_SIZE = SLOT_X_SIZE * 0.9
        Y_SIZE = SLOT_Y_SIZE * 0.1
        size = (X_SIZE, Y_SIZE)

    class CardPlace:
        X = (SLOT_X_SIZE - RoundSizes.CardSize.X_SIZE) / 2
        Y = SLOT_Y_SIZE * .12
        X_SIZE = RoundSizes.CardSize.X_SIZE
        Y_SIZE = RoundSizes.CardSize.Y_SIZE

        rect = (X, Y, X_SIZE, Y_SIZE)

    class DropButton:
        X_SIZE = scaled_w(0.04)
        Y_SIZE = SLOT_Y_SIZE * 0.15
        X = scaled_w(0.005)
        Y = SLOT_Y_SIZE * 0.84
