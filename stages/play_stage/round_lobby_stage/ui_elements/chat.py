from pygame.draw import rect as draw_rect
from visual.main_window import MAIN_SCREEN
from visual.UI_base.chat import Chat
from stages.play_stage.round_lobby_stage.settings.windows_sizes import LobbyWindowsSizes
from visual.UI_base.input_element_UI import InputElement
from visual.UI_base.button_UI import Button
from common.global_keyboard import GLOBAL_KEYBOARD
from settings.default_keys import Commands
from constants.server.network_keys import PlayerActions
from visual.UIController import UI_TREE
from common.global_mouse import GLOBAL_MOUSE
from obj_properties.rect_form import Rectangle


class ChatElement(Rectangle):
    def __init__(self, player_response):
        super().__init__(x=LobbyWindowsSizes.Chat.X,
                         y=LobbyWindowsSizes.Chat.Y,
                         size_x=LobbyWindowsSizes.Chat.X_SIZE,
                         size_y=LobbyWindowsSizes.Chat.Y_SIZE, )
        self.name = 'chat'
        self.player_response = player_response

        self.chat = Chat(x=LobbyWindowsSizes.Chat.ChatMessages.X,
                         y=LobbyWindowsSizes.Chat.ChatMessages.Y,
                         size_x=LobbyWindowsSizes.Chat.ChatMessages.X_SIZE,
                         size_y=LobbyWindowsSizes.Chat.ChatMessages.Y_SIZE,
                         )
        self.chat_input = InputElement(x=LobbyWindowsSizes.Chat.ChatInput.X,
                                       y=LobbyWindowsSizes.Chat.ChatInput.Y,
                                       size_x=LobbyWindowsSizes.Chat.ChatInput.X_SIZE,
                                       size_y=LobbyWindowsSizes.Chat.ChatInput.Y_SIZE,
                                       on_enter_action=self.send_message, max_letters_num=75,
                                       place_text_left=True, border_radius=5)

        self.clear_button = Button(x=LobbyWindowsSizes.Chat.ChatClearButton.X,
                                   y=LobbyWindowsSizes.Chat.ChatClearButton.Y,
                                   text='X', border_parameters={'border_radius': 5},
                                   size_x=LobbyWindowsSizes.Chat.ChatClearButton.X_SIZE,
                                   size_y=LobbyWindowsSizes.Chat.ChatClearButton.Y_SIZE,
                                   on_click_action=self.chat_input.clear,
                                   )

        UI_TREE.add_menu(self, self.chat)

    def update(self):
        self.chat_input.update()
        if Commands.Chat in GLOBAL_KEYBOARD.commands and not self.chat_input.is_focused:
            self.chat_input.focus()

        if self.collide_point(GLOBAL_MOUSE.pos):
            self.chat.update()
            self.clear_button.update()
            if GLOBAL_MOUSE.lmb:
                self.clear_button.click(GLOBAL_MOUSE.pos)

    def draw(self):
        self.chat.draw()
        self.chat_input.draw()
        self.clear_button.draw()
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)

    def send_message(self, inp):
        self.player_response[PlayerActions.MESSAGE] = inp.last_message

    def add_messages(self, messages: list):
        for message in messages:
            self.chat.add_message(message)