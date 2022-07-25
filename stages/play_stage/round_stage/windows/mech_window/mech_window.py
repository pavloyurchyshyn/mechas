from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from pygame.draw import line as draw_line
from pygame.draw import circle as draw_circle
# from settings_stage.UI_settings.menus_settings.settings_stage.mech_window import *
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes
from mechas.base.mech import BaseMech
from mechas.base.parts.body import BaseBody
from stages.play_stage.round_stage.windows.mech_window.settings import SlotSizes
from stages.play_stage.round_stage.windows.mech_window.slot_cell import VisualSlot, BodyVisualSlot
from settings.screen import Y_SCALE

from settings.global_parameters import test_draw_status_is_on

from visual.font_loader import DEFAULT_FONT


class MechWindow(Rectangle):
    def __init__(self, player_mech=None, x=RoundSizes.MechWindow.X, y=RoundSizes.MechWindow.Y,
                 size_x=RoundSizes.MechWindow.X_SIZE, size_y=RoundSizes.MechWindow.Y_SIZE):
        super(MechWindow, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.player_mech: BaseMech = player_mech

        self.mech_body: BaseBody = None
        self.mech_parts = []

        self.element_size = SlotSizes.X
        self.body_ui_slot: BodyVisualSlot = None
        self.calculate_side_positions()
        self.build_mech_UI()

    def calculate_side_positions(self):
        self.h_step = (self.size_x - SlotSizes.X * 3) / 4
        self.left_column = self.h_step
        self.midle_column = self.h_step + self.h_step + self.element_size
        self.right_column = self.h_step * 3 + self.element_size * 2

    def build_mech_UI(self):
        self.mech_parts.clear()
        if self.player_mech:
            self.mech_body: BaseBody = self.player_mech.body
            l_slots = [part for part in self.player_mech.left_slots.values()]
            r_slots = [part for part in self.player_mech.right_slots.values()]

            self.add_left_slots(l_slots)
            self.add_right_slots(r_slots)

            self.body_ui_slot = BodyVisualSlot(x=self.midle_column,
                                               y=self.y0 + (self.size_y - SlotSizes.X) / 2,
                                               size=SlotSizes.X, body=self.mech_body)

    def add_left_slots(self, slots: list):
        self.__build_column(self.left_column, slots)

    def add_right_slots(self, slots: list):
        self.__build_column(self.right_column, slots)

    def __build_column(self, x, slots):
        count = len(slots)

        step = (self.size_y - (count * SlotSizes.X)) / (count + 1)
        if step > 20 * Y_SCALE:
            step = 20 * Y_SCALE
        y = self.y0 + (self.size_y - count * SlotSizes.X - (count + 1) * step) / 2 + step

        for part in slots:
            r = VisualSlot(x=x, y=y, size=self.element_size, slot=part)

            self.mech_parts.append(r)
            y += self.element_size + step

    def get_start_y_and_step(self, count):
        step = (self.size_y - (count * SlotSizes.X)) / (count + 1)
        if step > 20 * Y_SCALE:
            step = 20 * Y_SCALE
        y = self.y0 + (self.size_y - count * SlotSizes.X - (count + 1) * step) / 2 + step

        return y, step

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
        for el in self.mech_parts:
            draw_rect(MAIN_SCREEN, (255, 255, 255), el.get_rect(), 1, 5)
            if el.is_full:
                text = DEFAULT_FONT.render(el.slot.detail.name, 1, (255, 255, 255))
                MAIN_SCREEN.blit(text, el.dots[-1])

        draw_rect(MAIN_SCREEN, (255, 255, 255), self.body_ui_slot.get_rect(), 1, 5)
        if self.body_ui_slot.is_full:
            text = DEFAULT_FONT.render(self.body_ui_slot.body.name, 1, (255, 255, 255))
            MAIN_SCREEN.blit(text, self.body_ui_slot.dots[-1])

        if test_draw_status_is_on():
            draw_line(MAIN_SCREEN, (0, 255, 0), self._dots[2], self._dots[-3])
            draw_line(MAIN_SCREEN, (0, 255, 0), self._dots[4], self._dots[-1])
            for dot in self._dots:
                draw_circle(MAIN_SCREEN, (255, 255, 0), dot, 3)
