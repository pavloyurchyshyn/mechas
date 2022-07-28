from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from pygame.draw import line as draw_line
from pygame.draw import circle as draw_circle
from constants.colors import simple_colors, RedButtonColors
from visual.sprites_functions import get_surface
from visual.UI_base.text_UI import Text
from visual.UI_base.button_UI import Button
from settings.screen import GAME_SCALE
from abc import abstractmethod

from mechas.base.parts.detail import BaseDetail
from mechas.base.parts.body import BaseBody
from mechas.base.slot import BaseSlot
from stages.play_stage.round_stage.windows.mech_window.settings import SlotSettings
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes


class BaseVisualSlot(Rectangle):
    def __init__(self, x, y, size_x=SlotSettings.X_SIZE, size_y=SlotSettings.Y_SIZE, slot=None):
        size_x = SlotSettings.X_SIZE if size_x is None else size_x
        size_y = SlotSettings.Y_SIZE if size_y is None else size_y
        super(BaseVisualSlot, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.slot = slot
        self.drop_button = None
        self.surface = None
        self.render()

    def render(self):
        self.surface = get_surface(*self.sizes, transparent=1)
        draw_rect(self.surface, simple_colors.grey3, (0, 0, *self.sizes), 0, SlotSettings.round_value)
        draw_rect(self.surface, simple_colors.white, (0, 0, *self.sizes), 1, SlotSettings.round_value)

        if self.is_full:
            Text(text=self.get_title(),
                 font_size=SlotSettings.Title.font_size,
                 y=SlotSettings.Title.Y,
                 screen=self.surface,
                 size=SlotSettings.Title.size,
                 )
            self.render_cards_position()

        self.drop_button = Button(x=SlotSettings.DropButton.X,
                                  y=SlotSettings.DropButton.Y,
                                  size_x=SlotSettings.DropButton.X_SIZE,
                                  size_y=SlotSettings.DropButton.Y_SIZE,
                                  text='Disconnect',
                                  screen=self.surface,
                                  border_parameters={'border_radius': 2},

                                  border_color=simple_colors.grey2,
                                  background_color=RedButtonColors.button_back_color,
                                  )

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def click(self, pos):
        raise NotImplementedError

    def render_cards_position(self):
        draw_rect(self.surface, simple_colors.white, SlotSettings.CardPlace.rect, 1, 5)

    def draw(self):
        MAIN_SCREEN.blit(self.surface, self.left_top)
        self.drop_button.draw()

    @abstractmethod
    def get_title(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def is_full(self) -> bool:
        raise NotImplementedError

    @property
    def is_empty(self) -> bool:
        return not self.is_full


class DetailVisualSlot(BaseVisualSlot):
    def __init__(self, x, y, size_x=None, size_y=None, slot: BaseSlot = None):
        super(DetailVisualSlot, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y, slot=slot)

    def update(self):
        self.drop_button.update()

    def click(self, pos):
        x, y = pos[0] - self.x0, pos[1] - self.y0
        self.drop_button.click((x, y))

    @property
    def is_full(self) -> bool:
        return self.slot.is_full

    def get_title(self) -> str:
        return self.slot.detail.verbal_name if self.slot.is_full else ''


class BodyVisualSlot(BaseVisualSlot):
    def __init__(self, x, y, size_x=None, size_y=None, body: BaseBody = None):
        super(BodyVisualSlot, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y, slot=body)

    def update(self):
        self.drop_button.update()

    def click(self, pos):
        x, y = pos[0] - self.x0, pos[1] - self.y0
        self.drop_button.click((x, y))

    @property
    def is_full(self) -> bool:
        return self.slot is not None

    def get_title(self) -> str:
        return self.slot.verbal_name if self.is_full else ''
