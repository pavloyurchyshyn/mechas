import os
import datetime

VERSION = '0.0.01'

FPS = 60

ROOT_OF_GAME = os.path.abspath(os.getcwd())

LOGS_FOLDER = os.path.join(ROOT_OF_GAME, 'logs')
SETTINGS_PATH = os.path.join(ROOT_OF_GAME, 'settings')

if not os.path.exists(SETTINGS_PATH):
    os.mkdir(SETTINGS_PATH)

SOUNDS_FOLDER = os.path.join(ROOT_OF_GAME, 'sounds')
SERVER_FOLDER = os.path.join(ROOT_OF_GAME, 'network')

COMMON_GAME_SETTINGS_JSON_PATH = 'common_game_settings.json'  # os.path.join(SETTINGS_PATH, 'common_game_settings.json')

PLAYER_NICKNAME_KEY = 'player_nickname'

# patterns
LOG_FILE_PATTERN = os.path.join(LOGS_FOLDER, '{}_' + datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S") + '.txt')
