from visual.UI_base.chat import Chat
from stages.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from visual.UI_base.input_element_UI import InputElement
from common.global_keyboard import GLOBAL_KEYBOARD
from settings.default_keys import Commands
from constants.network_keys import PlayerActions


class LobbyWindow:
    def __init__(self, player_response):
        self.player_response = player_response
        self.chat = Chat(x=LobbyWindowsSizes.Chat.X,
                         y=LobbyWindowsSizes.Chat.Y,
                         size_x=LobbyWindowsSizes.Chat.X_SIZE,
                         size_y=LobbyWindowsSizes.Chat.Y_SIZE,
                         )
        self.chat_input = InputElement(x=LobbyWindowsSizes.ChatInput.X, y=LobbyWindowsSizes.ChatInput.Y,
                                       size_x=LobbyWindowsSizes.ChatInput.X_SIZE,
                                       size_y=LobbyWindowsSizes.ChatInput.Y_SIZE,
                                       on_enter_action=self.send_message, max_letters_num=75,
                                       place_text_left=True, border_radius=5)

    def update(self):
        self.chat_input.update()
        if Commands.Chat in GLOBAL_KEYBOARD.commands and not self.chat_input.is_focused:
            self.chat_input.focus()

    def draw(self):
        self.chat.draw()
        self.chat_input.draw()

    def send_message(self, inp):
        self.chat.add_message(inp.last_message)
        self.player_response[PlayerActions.MESSAGE] = self.chat_input.last_message
