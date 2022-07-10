from settings.screen import scaled_w, scaled_h


class LobbyWindowsSizes:
    class Chat:
        X_SIZE = scaled_w(0.31)
        Y_SIZE = scaled_h(0.285 + 0.032)
        X = scaled_w(0.34)
        Y = scaled_h(0.68)

        class ChatMessages:
            X_SIZE = scaled_w(0.31)
            Y_SIZE = scaled_h(0.285)
            X = scaled_w(0.34)
            Y = scaled_h(0.68)

        class ChatInput:
            X_SIZE = scaled_w(0.30)
            Y_SIZE = scaled_h(0.032)
            X = scaled_w(0.34)
            Y = scaled_h(0.966)

        class ChatClearButton:
            X_SIZE = scaled_w(0.01)
            Y_SIZE = scaled_h(0.033)
            X = scaled_w(0.64)
            Y = scaled_h(0.967)

    class Players:
        X = scaled_w(0.75)
        Y = scaled_h(0.1)
        X_SIZE = scaled_w(0.25)
        Y_SIZE = scaled_h(0.35)

        class PlayerUIObj:
            X = scaled_w(0.75)
            Y = scaled_h(0.75)
            X_SIZE = scaled_w(0.25)
            Y_SIZE = scaled_h(0.25) // 10

            class KickButton:
                X = scaled_w(0.75)
                Y = scaled_h(0.75)
                X_SIZE = scaled_w(0.025)
                Y_SIZE = scaled_h(0.25) // 10

            # class Nickname:

    class GoButton:
        X = scaled_w(0.94)
        Y = scaled_h(0.94)
        X_SIZE = scaled_w(0.05)
        Y_SIZE = scaled_h(0.05)

    class ExitButton:
        X = scaled_w(0.967)
        Y = scaled_h(0.002)
        X_SIZE = scaled_w(0.03)
        Y_SIZE = scaled_h(0.03)