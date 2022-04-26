from common.logger import Logger
import traceback
import sys


class GameRunner:
    logger = Logger().LOGGER

    def __init__(self):
        self.clock = None
        self.font = None
        self.white = None
        self.main_screen = None
        self.stage = None

        self.draw_max_fps = self.draw_max_fps()
        self.draw_avg_fps = self.draw_avg_fps()
        self.draw_min_fps = self.draw_min_fps()

    def run(self):
        from settings.global_parameters import SET_CLIENT_INSTANCE

        SET_CLIENT_INSTANCE(1)

        from common.init_pygame import init_pygame  # do not remove its ok
        init_pygame()

        from pygame.time import Clock
        from pygame import event as EVENT
        from pygame import MOUSEBUTTONDOWN
        EVENT.set_allowed([MOUSEBUTTONDOWN, ])

        from pygame import display, draw, Surface, constants

        from constants.colors import WHITE
        from constants.game_stages import StagesConstants

        from settings.global_parameters import get_slow_motion_k, update_slow_motion, get_fps
        from settings.base import VERSION, FPS

        from visual.font_loader import DEFAULT_FONT
        from visual.main_window import MAIN_SCREEN, MAIN_SCREEN_RECT

        from common.global_clock import GLOBAL_CLOCK, ROUND_CLOCK
        from common.global_mouse import GLOBAL_MOUSE
        from common.global_keyboard import GLOBAL_KEYBOARD
        from common.stages import Stages

        from game_body import GameBody
        from time import time
        display.set_caption(f'V{VERSION}')

        clock = Clock()
        self.clock = clock
        self.font = DEFAULT_FONT
        self.white = WHITE
        self.main_screen = MAIN_SCREEN

        display.update(MAIN_SCREEN_RECT)

        self.stage = STAGES = Stages()

        G_Clock = GLOBAL_CLOCK
        R_Clock = ROUND_CLOCK
        G_Mouse = GLOBAL_MOUSE
        G_Keyboard = GLOBAL_KEYBOARD

        GAME_BODY = GameBody()
        start = time()

        while 1:
            events = EVENT.get()
            finish = time()

            clock.tick(get_fps())
            dt = finish - start
            start = finish
            # update time
            G_Clock.update(dt)
            if STAGES.current_stage == StagesConstants.ROUND_STAGE:
                update_slow_motion(d_time=dt)
                R_Clock.update(dt * get_slow_motion_k())

            # update mouse and keyboard
            G_Mouse.update()
            G_Keyboard.update(events)

            # scroll up and scroll down update
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        G_Mouse.scroll_top = 1

                    elif event.button == 5:
                        G_Mouse.scroll_bot = -1

            GAME_BODY.game_loop()

            fps = clock.get_fps()

            self.draw_fps(fps)
            self.draw_max_fps(fps, dt)
            self.draw_avg_fps(fps, dt)
            self.draw_min_fps(fps, dt)

            G_Mouse.draw()

            display.update(MAIN_SCREEN_RECT)
            MAIN_SCREEN.fill((0, 0, 0))

    def draw_fps(self, fps):
        fps_text = self.font.render(str(int(fps)), 1, self.white, (0, 0, 0))
        self.main_screen.blit(fps_text, (0, 0))

    def draw_max_fps(self):
        data = {'i': 0, 'max': '0'}

        def calc(fps, dt):
            if data['i'] > 3:
                data['i'] = 0
                data['max'] = '0'
            data['i'] += dt
            if int(data['max']) < fps:
                data['max'] = str(int(fps))
            fps_text = self.font.render(f"Max:{data['max']}", 1, self.white, (0, 0, 0))
            self.main_screen.blit(fps_text, (0, 30))

        return calc

    def draw_min_fps(self):
        data = {'i': 0, 'min': '999999'}

        def calc(fps, dt):
            if data['i'] > 3:
                data['i'] = 0
                data['min'] = '999999'
            data['i'] += dt
            if int(data['min']) > fps:
                data['min'] = str(int(fps))
            fps_text = self.font.render(f"Min:{data['min']}", 1, self.white, (0, 0, 0))
            self.main_screen.blit(fps_text, (0, 120))

        return calc

    def draw_avg_fps(self):
        data = {'i': 0, 'avg': [], 'all_avg': []}

        def calc(fps, dt):
            if data['i'] > 5:
                data['i'] = 0
                data['avg'].clear()
            data['i'] += dt
            data['avg'].append(fps)
            data['all_avg'].append(fps)
            avg = sum(data['avg']) // len(data['avg'])
            fps_text = self.font.render(f"AVG:{str(avg)}", 1, self.white, (0, 0, 0))
            self.main_screen.blit(fps_text, (0, 60))

            avg = sum(data['all_avg']) // len(data['all_avg'])
            fps_text = self.font.render(f"ALL AVG:{str(avg)}", 1, self.white, (0, 0, 0))
            self.main_screen.blit(fps_text, (0, 90))

        return calc


if __name__ == '__main__':
    try:
        game = GameRunner()
        game.run()
    except Exception as e:
        GameRunner.logger.error('Final fail')
        GameRunner.logger.error(e)
        GameRunner.logger.error(traceback.format_exc())
        GameRunner.logger.error(sys.exc_info()[2])
        # exit(1)
        del game
        raise e
