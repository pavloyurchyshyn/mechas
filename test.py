from importlib import import_module


print(import_module('game_text.ua.round_menu').ExitRound.exit)
print(import_module('game_text.en.round_menu').ExitRound.exit)
from datetime import datetime
print(datetime.now().strftime('%H:%M'))
