from pygame.draw import rect as draw_rect

from obj_properties.rect_form import Rectangle

from visual.sprites_functions import get_surface
from visual.UI_base.localization_mixin import LocalizationMixin
from visual.UI_base.button_UI import Button
from visual.main_window import MAIN_SCREEN
from visual.font_loader import custom_font

from common.singleton import Singleton
from common.global_mouse import GLOBAL_MOUSE
from stages.play_stage.round_stage.settings.exit_pop_up import *


class ExitPopUp(Rectangle, LocalizationMixin, metaclass=Singleton):
    name = RoundUINames.ExitPopUp
    id = RoundUINames.ExitPopUp

    def __init__(self, x=X_POS, y=Y_POS, size_x=POP_X_SIZE, size_y=POP_Y_SIZE):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.exit_yes = Button(**EXIT_YES)
        self.exit_no = Button(**EXIT_NO)

        self.surface = None
        self.render()

        self.active = False
        UI_TREE.add_menu(self, self.exit_yes, self.exit_no)

    def render(self):
        self.surface = get_surface(self.size_x, self.size_y, transparent=1, color=(0, 0, 0, 200))
        draw_rect(self.surface, (255, 255, 255), ((0, 0), (self.size_x, self.size_y)), 5, 5)
        EXIT_MESSAGE_SURF = custom_font(25).render(self.get_text_with_localization(RoundLocPaths.ExitPopUp), 1,
                                                   (255, 255, 255))
        x_size, y_size = EXIT_MESSAGE_SURF.get_size()
        self.surface.blit(EXIT_MESSAGE_SURF, (self.size_x / 2 - x_size / 2, y_size / 2))

    def update(self):
        if GLOBAL_MOUSE.lmb:
            if self.collide_point(GLOBAL_MOUSE.pos):
                for b in (self.exit_no, self.exit_yes):
                    if b.click(GLOBAL_MOUSE.pos):
                        break
            else:
                self.deactivate()

    def change_state(self, state):
        self.active = state

    def switch(self):
        self.change_state(not self.active)

    def activate(self):
        self.change_state(True)

    def deactivate(self):
        self.change_state(False)

    def draw(self):
        if self.active:
            MAIN_SCREEN.blit(self.surface, self.left_top)
            self.exit_yes.draw()
            self.exit_no.draw()
