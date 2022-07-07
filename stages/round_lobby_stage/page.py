from stages.round_lobby_stage.ui_elements.chat import ChatElement
from stages.round_lobby_stage.ui_elements.players_window import PlayersWindow
from visual.UI_base.button_UI import Button
from stages.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from common.global_mouse import GLOBAL_MOUSE
from common.global_keyboard import GLOBAL_KEYBOARD
from stages.round_lobby_stage.ui_elements.exit_pop_up import LobbyExitPopUp


class LobbyWindow:
    def __init__(self, player_response):
        self.player_response = player_response
        self.chat = ChatElement(player_response)
        self.players_window = PlayersWindow()

        self.exit_pop_up = LobbyExitPopUp()
        self.go_button = Button(text='Go',
                                x=LobbyWindowsSizes.GoButton.X,
                                y=LobbyWindowsSizes.GoButton.Y,
                                size_x=LobbyWindowsSizes.GoButton.X_SIZE,
                                size_y=LobbyWindowsSizes.GoButton.Y_SIZE
                                )

        self.exit_button = Button(text='X',
                                  x=LobbyWindowsSizes.ExitButton.X,
                                  y=LobbyWindowsSizes.ExitButton.Y,
                                  size_x=LobbyWindowsSizes.ExitButton.X_SIZE,
                                  size_y=LobbyWindowsSizes.ExitButton.Y_SIZE,
                                  on_click_action=self.exit_pop_up.switch,
                                  )

    def update(self):
        self.chat.update()
        self.players_window.update()

        if self.exit_pop_up.active:
            self.exit_pop_up.update()

        clicked = False
        for b in (self.go_button, self.exit_button):
            b.update()
            if GLOBAL_MOUSE.lmb and not clicked and not self.exit_pop_up.active:
                clicked = b.click(GLOBAL_MOUSE.pos)

        if GLOBAL_KEYBOARD.ESC:
            self.exit_pop_up.switch()

    def draw(self):
        self.chat.draw()
        self.players_window.draw()
        self.go_button.draw()
        self.exit_button.draw()

        self.exit_pop_up.draw()
