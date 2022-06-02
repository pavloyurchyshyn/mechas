from obj_properties.rect_form import Rectangle

from pygame.draw import rect as draw_rect

from settings.UI_setings.menus_settings.round_menu.windows_sizes import RoundSizes

from visual.UI_base.input_element_UI import InputElement
from visual.UI_base.chat import Chat
from visual.UI_base.button_UI import Button
from visual.UI_base.text_UI import Text
from visual.main_window import MAIN_SCREEN
from visual.UIController import UI_TREE

from common.global_mouse import GLOBAL_MOUSE

from constants.network_keys import PlayerActions


class ChatWindow(Rectangle):
    def __init__(self, player_response, x=RoundSizes.ChatWindow.X, y=RoundSizes.ChatWindow.Y,
                 size_x=RoundSizes.ChatWindow.X_SIZE, size_y=RoundSizes.ChatWindow.Y_SIZE):
        self.name = 'chat'
        self.player_response = player_response
        super(ChatWindow, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        input_y_size = 30
        self.messages = Chat(x=self.x0, y=self.y0,
                             size_x=self.size_x, size_y=self.size_y - input_y_size,
                             id='chat_input', )

        self.messages.add_message('Game started')

        self.input = InputElement(x=self.x0, y=self.y1 - input_y_size + 1,
                                  size_x=self.size_x * 0.955, size_y=input_y_size,
                                  on_enter_action=self.send_message, max_letters_num=75,
                                  place_text_left=True, border_radius=5)

        self.clear_button = Button(x=self.x0 + self.size_x * 0.945, y=self.y1 - input_y_size,
                                   text='X', border_parameters={'border_radius': 5},
                                   size_x=self.size_x * 0.05, size_y=input_y_size,
                                   on_click_action=lambda *args, **kwargs: self.input.clear(),
                                   )
        UI_TREE.add_menu(self, self.messages)

    def send_message(self, inp):
        print(inp.__dict__)
        self.player_response[PlayerActions.MESSAGE] = self.input.last_message

        # message = self.input.last_message
        # if message:
        #     self.player_response[PlayerActions.MESSAGE] = message

    def update(self):
        self.input.update()

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
