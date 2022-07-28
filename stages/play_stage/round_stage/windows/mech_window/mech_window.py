from obj_properties.rect_form import Rectangle
from pygame.draw import rect as draw_rect
from pygame.draw import line as draw_line
from pygame.draw import circle as draw_circle
# from settings_stage.UI_settings.menus_settings.settings_stage.mech_window import *
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes
from stages.play_stage.round_stage.windows.mech_window.settings import SlotSettings
from stages.play_stage.round_stage.windows.mech_window.visual_slot import DetailVisualSlot, BodyVisualSlot

from mechas.base.mech import BaseMech
from mechas.base.parts.body import BaseBody

from settings.screen import Y_SCALE
from settings.global_parameters import test_draw_status_is_on
from visual.main_window import MAIN_SCREEN
from common.global_mouse import GLOBAL_MOUSE
from visual.font_loader import DEFAULT_FONT


class MechWindow(Rectangle):
    def __init__(self, player=None, x=RoundSizes.MechWindow.X, y=RoundSizes.MechWindow.Y,
                 size_x=RoundSizes.MechWindow.X_SIZE, size_y=RoundSizes.MechWindow.Y_SIZE):
        super(MechWindow, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.player = player
        self.player_mech: BaseMech = player.mech

        self.mech_body: BaseBody = None
        self.mech_parts = []

        # self.element_size = SlotSizes.X_SIZE
        self.body_ui_slot: BodyVisualSlot = None
        self.calculate_side_positions()

        self.build_mech_UI()

    def update(self):
        clicked = False

        for slot in self.mech_parts:
            slot.update()
            if not clicked and GLOBAL_MOUSE.lmb:
                if slot.collide_point(GLOBAL_MOUSE.pos):
                    clicked = True
                    slot.click(GLOBAL_MOUSE.pos)

        if not clicked and GLOBAL_MOUSE.lmb:
            if self.body_ui_slot.collide_point(GLOBAL_MOUSE.pos):
                self.body_ui_slot.update()
                self.body_ui_slot.click(GLOBAL_MOUSE.pos)

    def calculate_side_positions(self):
        self.h_step = (self.size_x - SlotSettings.X_SIZE * 3) / 4
        self.left_column = self.h_step
        self.midle_column = self.h_step + self.h_step + SlotSettings.X_SIZE
        self.right_column = self.h_step * 3 + SlotSettings.X_SIZE * 2

    def build_mech_UI(self):
        self.mech_parts.clear()
        if self.player_mech:
            self.mech_body: BaseBody = self.player_mech.body
            l_slots = [part for part in self.player_mech.left_slots.values()]
            r_slots = [part for part in self.player_mech.right_slots.values()]

            self.add_left_slots(l_slots)
            self.add_right_slots(r_slots)
            self.body_ui_slot = BodyVisualSlot(x=self.midle_column,
                                               y=self.y0 + (self.size_y - SlotSettings.X_SIZE) / 2,
                                               body=self.mech_body)

    def add_left_slots(self, slots: list):
        self.__build_column(self.left_column, slots)

    def add_right_slots(self, slots: list):
        self.__build_column(self.right_column, slots)

    def __build_column(self, x, slots):
        y, step = self.get_start_y_and_step(len(slots))
        for part in slots:
            r = DetailVisualSlot(x=x, y=y, size_x=SlotSettings.X_SIZE, size_y=SlotSettings.Y_SIZE, slot=part)

            self.mech_parts.append(r)
            y += SlotSettings.Y_SIZE + step

    def get_start_y_and_step(self, count):
        step = (self.size_y - (count * SlotSettings.Y_SIZE)) / (count + 1)
        if step > SlotSettings.MIN_STEP_BETWEEN_SLOTS * Y_SCALE:
            step = SlotSettings.MIN_STEP_BETWEEN_SLOTS * Y_SCALE
        y = self.y0 + (self.size_y - count * SlotSettings.Y_SIZE - (count + 1) * step) / 2 + step

        return y, step

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
        for el in self.mech_parts:
            el.draw()

        self.body_ui_slot.draw()

        if test_draw_status_is_on():
            draw_line(MAIN_SCREEN, (0, 255, 0), self._dots[2], self._dots[-3])
            draw_line(MAIN_SCREEN, (0, 255, 0), self._dots[4], self._dots[-1])
            for dot in self._dots:
                draw_circle(MAIN_SCREEN, (255, 255, 0), dot, 3)
