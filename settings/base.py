import os
import datetime

VERSION = '0.0.01'

ROOT_OF_GAME = os.path.abspath(os.getcwd())

LOGS_FOLDER = os.path.join(ROOT_OF_GAME, 'logs')
SETTINGS_PATH = os.path.join(ROOT_OF_GAME, 'settings')
LOCALIZATIONS_FOLDER = os.path.join(ROOT_OF_GAME, 'localization')

if not os.path.exists(SETTINGS_PATH):
    os.mkdir(SETTINGS_PATH)

SOUNDS_FOLDER = os.path.join(ROOT_OF_GAME, 'sounds')
SERVER_FOLDER = os.path.join(ROOT_OF_GAME, 'client_server_parts')

COMMON_CONFIG_PATH = os.path.join(SETTINGS_PATH, 'common_config.json')
KEYS_CONFIG_FILE = os.path.join(SETTINGS_PATH, 'keyboard_config.json')

# patterns
LOG_FILE_PATTERN = os.path.join(LOGS_FOLDER, '{}_.txt')
# LOG_FILE_PATTERN = os.path.join(LOGS_FOLDER, '{}_' + datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S") + '.txt')
