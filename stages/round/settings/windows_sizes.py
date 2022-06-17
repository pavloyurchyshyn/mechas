from settings.screen import SCREEN_H, SCREEN_W, HALF_SCREEN_W, HALF_SCREEN_H, GAME_SCALE, X_SCALE, Y_SCALE


def scaled_w(percent):
    return SCREEN_W * percent


def scaled_h(percent):
    return SCREEN_H * percent


class RoundSizes:
    class TopBar:
        X = 0
        Y = 0
        X_SIZE = SCREEN_W
        Y_SIZE = scaled_h(0.03)

        EXIT_B_X_SIZE = 50 * X_SCALE
        EXIT_B_Y_SIZE = Y_SIZE
        EXIT_B_X = SCREEN_W - 2 - EXIT_B_X_SIZE
        EXIT_B_Y = Y

    class MechWindow:
        X = 0
        Y = scaled_h(0.03) - 1
        X_SIZE = scaled_w(0.25)
        Y_SIZE = scaled_h(0.65)

    class WorldWindow:
        X_SIZE = scaled_w(0.44)
        Y_SIZE = scaled_h(0.7)
        X = scaled_w(0.25) - 1
        Y = scaled_h(0.03)

    class SkillsCards:
        X = scaled_w(0.25) - 1
        Y = scaled_h(0.76)
        X_SIZE = scaled_w(0.36)
        Y_SIZE = scaled_h(0.12)

    class UsedSkillsCards:
        X = scaled_w(0.25) - 1
        Y = scaled_h(0.88)
        X_SIZE = scaled_w(0.36)
        Y_SIZE = scaled_h(0.12)

    class ChatWindow:
        X = scaled_w(0.69)
        Y = scaled_h(0.68)
        X_SIZE = scaled_w(0.31)
        Y_SIZE = scaled_h(0.32)

    class ReadyBody:
        X = scaled_w(0.61)
        Y = scaled_h(0.88)
        X_SIZE = scaled_w(0.08)
        Y_SIZE = scaled_h(0.12)

        class ReadyButton:
            X = scaled_w(0.61) + 2
            Y = scaled_h(0.97) + 1
            X_SIZE = scaled_w(0.08)
            Y_SIZE = scaled_h(0.03)
            border_parameters = {'border_radius': 5}

    class Dice:
        X = scaled_w(0.61) + 1
        Y = scaled_h(0.76) + 1
        X_SIZE = scaled_w(0.08) - 1
        Y_SIZE = scaled_h(0.12)