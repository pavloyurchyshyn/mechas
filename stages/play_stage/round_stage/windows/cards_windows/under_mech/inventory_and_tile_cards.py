from stages.play_stage.round_stage.windows.cards_windows.under_mech.tile_cards import TileCards
from stages.play_stage.round_stage.windows.cards_windows.under_mech.inventory_cards import InventoryCards
from stages.play_stage.round_stage.windows.cards_windows.arrow import CardUseArrow


# TODO
class InventoryAndTileCards:
    def __init__(self):
        self.tile_cards = TileCards()
        self.inventory = InventoryCards()

        self.arrow = CardUseArrow(self.tile_cards, self.inventory)

    def update(self):
        self.arrow.update()
        self.tile_cards.update()
        self.inventory.update()

    def draw(self):
        self.arrow.draw()
        self.tile_cards.draw()
        self.inventory.draw()
