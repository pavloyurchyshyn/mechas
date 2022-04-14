from obj_properties.rect_form import Rectangle
from settings.screen import SCREEN_H, SCREEN_W
from pygame.draw import lines as draw_lines
from visual.main_window import MAIN_SCREEN


class RoundUI:
    screen_w = SCREEN_W
    screen_h = SCREEN_H

    def __init__(self):
        self.top_bar = Rectangle(x=0, y=0, size_x=SCREEN_W, size_y=self.get_rel_h(0.025))

        self.world_data_rect = Rectangle(x=0, y=self.get_rel_h(0.025), size_x=self.get_rel_h(0.7),
                                         size_y=self.get_rel_h(0.05))
        self.world_rect = Rectangle(x=0, y=self.world_data_rect.y1,
                                    size_x=self.get_rel_h(0.7), size_y=self.get_rel_h(0.7))

        self.actions_log_rect = Rectangle(x=0, y=self.world_rect.y1, size_x=self.world_rect.size_x,
                                          size_y=SCREEN_H - self.world_rect.y1)

        self.cards_rect = Rectangle(x=self.get_rel_w(0.75), y=self.top_bar.y1,
                                    size_x=self.get_rel_w(0.5), size_y=self.get_rel_h(0.7)
                                    )

        self.chat_rect = Rectangle(x=self.cards_rect.x0, y=self.cards_rect.y1,
                                   size_x=self.cards_rect.size_x, size_y=self.cards_rect.size_x)

        self._my_robot_rect = Rectangle(self.world_rect.x1, self.top_bar.y1,
                                        size_x=self.cards_rect.x0 - self.world_rect.x1,
                                        size_y=(SCREEN_H - self.top_bar.y1) / 2)
        self.other_robots_rect = Rectangle(self.world_rect.x1, self._my_robot_rect.y1,
                                           size_x=self.cards_rect.x0 - self.world_rect.x1,
                                           size_y=(SCREEN_H - self.top_bar.y1) / 2)

        # self.arena_window = ArenaWindow(x=self.world_rect.x0,
        #                                 y=self.world_rect.y0,
        #                                 size_x=self.world_rect.size_x)

    def update(self):
        pass
        #self.arena_window.update()

    def draw(self):
        #self.arena_window.draw()

        for r in (self.top_bar, self.world_rect, self.chat_rect,
                  self.cards_rect, self.world_data_rect, self.actions_log_rect,
                  self._my_robot_rect, self.other_robots_rect,
                  ):
            draw_lines(MAIN_SCREEN, (55, 55, 255), 1, r._dots[1:])

    def get_rel_h(self, rel_val):
        return self.screen_h * rel_val

    def get_rel_w(self, rel_val):
        return self.screen_w * rel_val
