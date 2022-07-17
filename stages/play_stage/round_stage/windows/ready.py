from pygame.draw import rect as draw_rect

from obj_properties.rect_form import Rectangle
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes
from visual.main_window import MAIN_SCREEN
from visual.UI_base.button_UI import Button
from visual.UI_base.text_UI import Text
from common.global_mouse import GLOBAL_MOUSE
from common.global_clock import ROUND_CLOCK
from common.logger import Logger

from settings.localization import LocalizationLoader
from constants.network_keys import PlayerActions, ServerResponseCategories
from constants.colors import simple_colors

LOGGER = Logger()

localization = LocalizationLoader()
menu_text = localization.text.UI.round.ready_body


class ReadyWindow(Rectangle):
    emergency_time = -10.

    def __init__(self, player_response):
        super(ReadyWindow, self).__init__(x=RoundSizes.ReadyBody.X, y=RoundSizes.ReadyBody.Y,
                                          size_x=RoundSizes.ReadyBody.X_SIZE, size_y=RoundSizes.ReadyBody.Y_SIZE,
                                          )
        self.ready_button = Button(x=RoundSizes.ReadyBody.ReadyButton.X,
                                   y=RoundSizes.ReadyBody.ReadyButton.Y,
                                   size_x=RoundSizes.ReadyBody.ReadyButton.X_SIZE,
                                   size_y=RoundSizes.ReadyBody.ReadyButton.Y_SIZE,
                                   text=menu_text.ready_button,
                                   text_color=(100, 255, 100),
                                   on_click_action=self.ready_click,
                                   change_after_click=False,
                                   non_active_after_click=False,
                                   border_parameters=RoundSizes.ReadyBody.ReadyButton.border_parameters,
                                   )
        self.ready_button.change_picture(0)

        self.timer = Text(text='00:00', font_size=22,
                          x=RoundSizes.ReadyBody.TimerText.X, y=RoundSizes.ReadyBody.TimerText.Y,
                          )

        self.ready_count = Text(text='0/0', font_size=30,
                                x=RoundSizes.ReadyBody.ReadyCount.X, y=RoundSizes.ReadyBody.ReadyCount.Y,
                                )

        self.player_response = player_response
        self.ready_status = False

    def ready_click(self):
        self.player_response[PlayerActions.READY_STATUS] = not self.ready_status

    def update(self):
        self.ready_button.update()
        if GLOBAL_MOUSE.lmb:
            self.ready_button.click(GLOBAL_MOUSE.pos)

    def process_server_data(self, data):
        self.update_ready(data)

    def process_time(self, data):
        if ServerResponseCategories.MatchTime in data:
            ROUND_CLOCK.set_time(*data.pop(ServerResponseCategories.MatchTime))
            if ROUND_CLOCK.str_time != self.timer.text:
                self.timer.change_text(ROUND_CLOCK.str_time)
                if ROUND_CLOCK.time > self.emergency_time:
                    self.timer.change_color(simple_colors.red)
                else:
                    self.timer.change_color(simple_colors.white)

    def update_ready(self, data):
        if ServerResponseCategories.ReadyState in data:
            ready = data.pop(ServerResponseCategories.ReadyState)
            LOGGER.info(f'Ready status changed to {ready}')

            self.ready_status = ready
            # self.ready_button.active = ready
            self.ready_button.change_picture(ready)

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
        self.ready_button.draw()
        self.timer.draw()
        self.ready_count.draw()
