from settings.screen import SCREEN_H, SCREEN_W, scaled_w, scaled_h, X_SCALE


class RoundSizes:
    class TopBar:
        X = 0
        Y = 0
        X_SIZE = SCREEN_W
        Y_SIZE = scaled_h(0.03)

        EXIT_B_X_SIZE = scaled_w(0.03)
        EXIT_B_Y_SIZE = Y_SIZE - 2
        EXIT_B_X = SCREEN_W - EXIT_B_X_SIZE
        EXIT_B_Y = Y + 1

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
        Y = scaled_h(0.881)
        X_SIZE = scaled_w(0.08)
        Y_SIZE = scaled_h(0.12)

        class ReadyButton:
            X = scaled_w(0.61) + 2
            Y = scaled_h(0.97)
            X_SIZE = scaled_w(0.078)
            Y_SIZE = scaled_h(0.03)
            border_parameters = {'border_radius': 5}

        class TimerText:
            X = scaled_w(0.635)
            Y = scaled_h(0.88)

        class ReadyCount:
            X = scaled_w(0.635)
            Y = scaled_h(0.92)

    class Dice:
        X = scaled_w(0.61) + 1
        Y = scaled_h(0.76) + 1
        X_SIZE = scaled_w(0.08) - 1
        Y_SIZE = scaled_h(0.12)

    class Bars:
        X_SIZE = scaled_w(0.36)
        Y_SIZE = scaled_h(0.015)

        class Mana:
            X = scaled_w(0.25)
            Y = scaled_h(0.745)

            text_pos = scaled_w(0.612), scaled_h(0.745)
            reg_text_pos = scaled_w(0.672), scaled_h(0.745)

        class HP:
            X = scaled_w(0.25)
            Y = scaled_h(0.73)

            text_pos = scaled_w(0.612), scaled_h(0.73)
            reg_text_pos = scaled_w(0.672), scaled_h(0.73)
