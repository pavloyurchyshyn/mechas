from stages.play_stage.round_stage.windows.cards_windows.tile_cards import TileCards
from stages.play_stage.round_stage.windows.cards_windows.cards_in_hand import CardsInHands

# TODO
class InventoryAndTileCards:
    def __init__(self):
        self.tile_cards = TileCards()
        self.inventory = CardsInHands()

    def draw(self):
        self.tile_cards.draw()
        self.inventory.draw()
