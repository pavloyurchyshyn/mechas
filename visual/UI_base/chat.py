from common.global_mouse import GLOBAL_MOUSE
from visual.sprites_functions import get_surface
from obj_properties.rect_form import Rectangle
from visual.UI_base.text_UI import Text
from visual.main_window import MAIN_SCREEN


class Chat(Rectangle):
    ALL = 'all'

    def __init__(self, x, y, size_x, size_y, elements=[], id=None):
        self.id = id
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)
        self.surface = get_surface(size_x, size_y, transparent=1, color=(255, 255, 255, 50))
        self.elements: list = elements

        self.current_category = Chat.ALL

        self.by_categories: dict = {}
        self.scroll = 0
        self.elements_height = 0

    def update(self):
        if self.collide_point(GLOBAL_MOUSE.pos):
            if GLOBAL_MOUSE.scroll and self.elements_height > self.size_y:
                self.scroll -= GLOBAL_MOUSE.scroll * 2

                if self.scroll > 0:
                    self.scroll = 0

                if self.size_y - self.elements_height > self.scroll:
                    self.scroll = self.size_y - self.elements_height

                self.render()

    def render(self):
        self.calculate_height()
        self.surface.fill((255, 255, 255, 50))

        h = self.size_y - self.scroll

        for el in reversed(self.elements):
            h -= el.size[1]
            el.set_y(h)
            el.draw()

    def calculate_height(self):
        self.elements_height = 0
        for el in self.elements:
            self.elements_height += el.size[1]

    def add_message(self, text, category=None, build=True):
        category = Chat.ALL if category is not None else category

        text_ = Text(text=text, screen=self.surface, x=1,
                     place_left=True, place_bot=True, place_inside=False, raw_text=True)

        self.elements.append(text_)

        if category not in self.by_categories:
            self.by_categories[category] = [text_, ]
        else:
            self.by_categories[category].append(text_)

        if build:
            self.render()

    def draw(self):
        MAIN_SCREEN.blit(self.surface, self.left_top)
