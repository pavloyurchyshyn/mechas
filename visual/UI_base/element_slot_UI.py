from obj_properties.rect_form import Rectangle
from visual.main_window import MAIN_SCREEN
from pygame.draw import rect as draw_rect


class UIObjSlot(Rectangle):
    def __init__(self, x, y, size_x, size_y=None, ui_obj=None):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.ui_obj = ui_obj

    def update(self):
        pass

    def draw(self):
        if self.ui_obj:
            self.ui_obj.draw()
        draw_rect(MAIN_SCREEN, (255, 255, 255), self.get_rect(), 1, 5)

    def set_obj(self, obj):
        self.ui_obj = obj