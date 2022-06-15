from common.sound_loader import GLOBAL_MUSIC_PLAYER
from visual.UI_base.progress_bar_UI import ProgressBar
from visual.main_window import MAIN_SCREEN
from settings.screen import X_SCALE, Y_SCALE


from constants.colors import WHITE, GREY_DARK_2

VOLUME_PROGRESS_BAR = ProgressBar(screen=MAIN_SCREEN,
                                  stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                  stages_num=GLOBAL_MUSIC_PLAYER.volume_stages,
                                  bar_pos=(300*X_SCALE, 125*Y_SCALE),
                                  bar_inner_color=GREY_DARK_2 if GLOBAL_MUSIC_PLAYER.muted else WHITE,
                                  bar_x_size=200, bar_y_size=10)
