from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
from pygame.draw import line as draw_line
from pygame.draw import circle as draw_circle
# from settings_stage.UI_settings.menus_settings.settings_stage.mech_window import *
from game_logic.stages.round_stage.settings.windows_sizes import RoundSizes
from mechas.base.mech import BaseMech
from mechas.base.parts.body import BaseBody
from game_logic.stages.round_stage.windows.mech_window.settings import SlotSizes
from settings.screen import Y_SCALE

from settings.global_parameters import test_draw_status_is_on


class MechWindow(Rectangle):
    def __init__(self, player_mech=None, x=RoundSizes.MechWindow.X, y=RoundSizes.MechWindow.Y,
                 size_x=RoundSizes.MechWindow.X_SIZE, size_y=RoundSizes.MechWindow.Y_SIZE):
        super(MechWindow, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.player_mech = player_mech

        self.mech_body: BaseMech = None
        self.mech_parts = []

        self.element_size = SlotSizes.X
        self.body_ui_slot = None
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
            self.mech_body: BaseBody = self.player_mech

            l_parts = [parts for parts in [getattr(self.mech_body, s) for s in BaseBody.Sides.left_parts]]
            r_parts = [parts for parts in [getattr(self.mech_body, s) for s in BaseBody.Sides.right_parts]]

            self.add_left_parts(l_parts)
            self.add_right_part(r_parts)

            self.mech_parts.append(
                Rectangle(x=self.midle_column, y=self.y0 + (self.size_y - SlotSizes.X) / 2, size_x=SlotSizes.X))

    def add_left_parts(self, parts: list):
        x = self.left_column
        count = 0
        for items in parts:
            count += len(items)

        step = (self.size_y - (count * SlotSizes.X)) / (count + 1)
        if step > 20 * Y_SCALE:
            step = 20 * Y_SCALE
        y = self.y0 + (self.size_y - count * SlotSizes.X - (count + 1) * step) / 2 + step

        for parts_ in parts:
            for part in parts_:
                r = Rectangle(x=x, y=y, size_x=self.element_size)
                self.mech_parts.append(r)
                y += self.element_size + step

    def add_right_part(self, parts):
        x = self.right_column

        count = 0
        for items in parts:
            count += len(items)

        step = (self.size_y - (count * SlotSizes.X)) / (count + 1)
        if step > 20 * Y_SCALE:
            step = 20 * Y_SCALE
        y = self.y0 + (self.size_y - count * SlotSizes.X - (count + 1) * step) / 2 + step

        for parts_ in parts:
            for part in parts_:
                # TODO add part ui element
                r = Rectangle(x=x, y=y, size_x=self.element_size)
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

        if test_draw_status_is_on():
            draw_line(MAIN_SCREEN, (0, 255, 0), self._dots[2], self._dots[-3])
            draw_line(MAIN_SCREEN, (0, 255, 0), self._dots[4], self._dots[-1])
            for dot in self._dots:
                draw_circle(MAIN_SCREEN, (255, 255, 0), dot, 3)
