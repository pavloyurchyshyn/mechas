from time import time as current_time
from common.save_and_load_json_config import get_from_common_config, save_to_common_config


__all__ = [
    'get_language', 'set_fps', 'get_fps', 'set_slow_motion', 'its_client_instance', 'pause_step',
    'update_slow_motion', 'SET_CLIENT_INSTANCE', 'get_slow_motion_k', 'change_test_draw_status',
    'test_draw_status_is_on',
]

GLOBAL_SETTINGS = {
    'test_draw': 1,
    'client_instance': 0,
    'slow_motion': 0,
    'slow_motion_value': 0.05,
    'fps': get_from_common_config('fps_config', 60),
    'language': get_from_common_config('language', 'eng'),

}


def get_language():
    return GLOBAL_SETTINGS['language']


def set_language(lang):
    GLOBAL_SETTINGS['language'] = lang
    save_to_common_config('language', lang)


def set_fps(fps):
    GLOBAL_SETTINGS['fps'] = fps
    save_to_common_config('fps_config', fps)


def get_fps():
    return GLOBAL_SETTINGS['fps']


DEFAULT_SLOW_TIME_DURATION = 10


def set_slow_motion(value=DEFAULT_SLOW_TIME_DURATION):
    GLOBAL_SETTINGS['slow_motion'] = value


def update_slow_motion(d_time):
    if GLOBAL_SETTINGS['slow_motion'] > 0:
        GLOBAL_SETTINGS['slow_motion'] -= d_time


def get_slow_motion_k():
    if GLOBAL_SETTINGS['slow_motion'] > 0:
        return GLOBAL_SETTINGS['slow_motion_value']
    else:
        return 1


def SET_CLIENT_INSTANCE(v=1):
    GLOBAL_SETTINGS['client_instance'] = v


def its_client_instance():
    return GLOBAL_SETTINGS['client_instance']


def pause_step():
    GLOBAL_SETTINGS['next_pause'] = GLOBAL_SETTINGS['pause_delay'] + current_time()


def change_test_draw_status():
    GLOBAL_SETTINGS['test_draw'] = not GLOBAL_SETTINGS['test_draw']


def test_draw_status_is_on():
    return GLOBAL_SETTINGS['test_draw']
