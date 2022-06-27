from obj_properties.rect_form import Rectangle

from pygame.draw import rect as draw_rect

from game_logic.stages.round_stage.settings.windows_sizes import RoundSizes

from visual.UI_base.input_element_UI import InputElement
from visual.UI_base.chat import Chat
from visual.UI_base.button_UI import Button
from visual.main_window import MAIN_SCREEN
from visual.UIController import UI_TREE

from common.global_mouse import GLOBAL_MOUSE
from common.global_keyboard import GLOBAL_KEYBOARD

from constants.network_keys import PlayerActions
from settings.default_keys import Commands


class ChatWindow(Rectangle):
    def __init__(self, player_response, x=RoundSizes.ChatWindow.X, y=RoundSizes.ChatWindow.Y,
                 size_x=RoundSizes.ChatWindow.X_SIZE, size_y=RoundSizes.ChatWindow.Y_SIZE):
        self.name = 'chat'
        self.player_response = player_response
        super(ChatWindow, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        clean_x_size = self.size_x * 0.055
        clean_y_size = self.size_y * 0.1
        self.messages = Chat(x=self.x0, y=self.y0,
                             size_x=self.size_x, size_y=self.size_y - clean_y_size,
                             id='chat_input', )

        self.input = InputElement(x=self.x0, y=self.y1 - clean_y_size,
                                  size_x=self.size_x - clean_x_size, size_y=clean_y_size,
                                  on_enter_action=self.send_message, max_letters_num=75,
                                  place_text_left=True, border_radius=5)

        self.clear_button = Button(x=self.x1 - clean_x_size - 1, y=self.y1 - clean_y_size,
                                   text='X', border_parameters={'border_radius': 5},
                                   size_x=clean_x_size, size_y=clean_y_size,
                                   on_click_action=self.input.clear,
                                   )
        UI_TREE.add_menu(self, self.messages)

    def send_message(self, inp):
        self.player_response[PlayerActions.MESSAGE] = self.input.last_message

    def update(self):
        self.input.update()
        if Commands.Chat in GLOBAL_KEYBOARD.commands and not self.input.is_focused:
            self.input.focus()

        if self.collide_point(GLOBAL_MOUSE.pos):
            self.messages.update()
            self.clear_button.update()
            if GLOBAL_MOUSE.lmb:
                self.clear_button.click(GLOBAL_MOUSE.pos)

    def add_messages(self, messages: list):
        for message in messages:
            self.messages.add_message(message)

    def draw(self):
        self.input.draw()
        self.messages.draw()
        self.clear_button.draw()
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 4)
