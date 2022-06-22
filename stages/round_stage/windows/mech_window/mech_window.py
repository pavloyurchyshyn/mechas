from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect
# from settings_stage.UI_settings.menus_settings.settings_stage.mech_window import *
from stages.round_stage.settings.windows_sizes import RoundSizes
from mechas.base.mech import BaseMech
from mechas.base.body import BaseBody


class MechWindow(Rectangle):
    def __init__(self, player_mech=None, x=RoundSizes.MechWindow.X, y=RoundSizes.MechWindow.Y,
                 size_x=RoundSizes.MechWindow.X_SIZE, size_y=RoundSizes.MechWindow.Y_SIZE):
        super(MechWindow, self).__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.player_mech = player_mech

        self.mech_body: BaseMech = None
        self.mech_parts = []

        self.body_ui_slot = None
        self.build_mech_UI()

    def build_mech_UI(self):
        self.mech_parts.clear()
        if self.player_mech:
            self.mech_body: BaseBody = self.player_mech

            l_parts = [parts for parts in [getattr(self.mech_body, s) for s in BaseBody.Sides.left_parts]]
            r_parts = [parts for parts in [getattr(self.mech_body, s) for s in BaseBody.Sides.right_parts]]
            self.add_left_parts(l_parts)
            self.add_right_part(r_parts)

    def add_left_parts(self, parts):
        x = 5
        y = self.y0 + 5

        for parts_ in parts:
            for part in parts_:
                r = Rectangle(x=x, y=y, size_x=50)
                self.mech_parts.append(r)
                y += 55

    def add_right_part(self, parts):
        x = 50
        y = self.y0 + 5

        for parts_ in parts:
            for part in parts_:
                # TODO add part ui element
                r = Rectangle(x=x, y=y, size_x=50)
                self.mech_parts.append(r)
                y += 55

    def draw(self):
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)
        for el in self.mech_parts:
            draw_rect(MAIN_SCREEN, (255, 255, 255), el.get_rect(), 1, 5)
