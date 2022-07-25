from stages.play_stage.round_stage.windows.world_window.window import ArenaWindow
from stages.play_stage.round_stage.windows.top_bar import TopBar
from stages.play_stage.round_stage.windows.exit_pop_up import ExitPopUp
from stages.play_stage.round_stage.windows.cards_windows.under_world.cards_window import CardsWindow
from stages.play_stage.round_stage.windows.cards_windows.under_mech.inventory_and_tile_cards import InventoryAndTileCards
from stages.play_stage.round_stage.windows.mech_window.mech_window import MechWindow
from stages.play_stage.round_stage.windows.chat import ChatWindow
from stages.play_stage.round_stage.windows.ready import ReadyWindow
from stages.play_stage.round_stage.windows.dice import DiceWindow
from stages.play_stage.round_stage.mech_visual.mech import MechVisual
from stages.play_stage.round_stage.windows.bars_windows.bars import BarsLogic
from stages.play_stage.round_stage.windows.cards_windows.deck_of_cards import DeckOfCardsWindow


from constants.server.network_keys import ServerResponseCategories

from common.global_keyboard import GLOBAL_KEYBOARD
from visual.UIController import UI_TREE
from game_logic.components.player_object import Player


class Round:
    name = 'round'

    def __init__(self, player: Player, other_players: dict, players_num: int):
        self.player_response = {}

        self.player = player
        self.other_players = other_players

        self.arena_window = ArenaWindow()
        self.top_bar = TopBar()
        self.exit_pop_up = ExitPopUp()
        self.cards_window = CardsWindow(mech=player.mech)
        self.inventory_and_tile_cards_window = InventoryAndTileCards()
        self.mech_window = MechWindow(player_mech=player.mech)
        self.chat_window = ChatWindow(self.player_response)
        self.dice = DiceWindow()
        self.mech_visual = MechVisual(mech=self.mech, world=self.arena_window.visual_world)
        self.mana_and_hp_bars = BarsLogic(mech=self.mech)
        self.decks = DeckOfCardsWindow()
        self.ready = ReadyWindow(self.player_response, players_num)

        UI_TREE.add_menu(self, self.exit_pop_up)

    def update(self):
        # that a local update for player actions
        if GLOBAL_KEYBOARD.ESC:
            self.exit_pop_up.switch()

        if self.exit_pop_up.active:
            self.exit_pop_up.update()
        else:
            self.arena_window.update()
            self.top_bar.update()

        self.chat_window.update()
        self.ready.update()

    def draw(self):
        self.arena_window.draw()

        self.top_bar.draw()

        self.exit_pop_up.draw()
        self.decks.draw()

        self.cards_window.draw()
        self.inventory_and_tile_cards_window.draw()

        self.mech_window.draw()
        self.chat_window.draw()

        self.ready.draw()
        self.dice.draw()
        self.mech_visual.draw()

        self.mana_and_hp_bars.draw()

    def set_player(self, player):
        self.player = player

    def add_other_player(self, token, player):
        self.other_players[token] = player

    def replace_other_player(self, old_token, new_token):
        self.other_players[new_token] = self.other_players.pop(old_token)

    @property
    def mech(self):
        return self.player.mech

    def process_server_data(self, data: dict):
        # that update for received data
        self.chat_window.add_messages(data.pop(ServerResponseCategories.MessagesToAll, {}))
        this_player_data = data.pop(ServerResponseCategories.PlayersUpdates, {}).pop(self.player.token, {})
        self.ready.process_server_data(data, this_player_data)


