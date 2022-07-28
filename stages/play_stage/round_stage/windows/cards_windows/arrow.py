from visual.cards.skill_card import SkillCard
from common.global_mouse import GLOBAL_MOUSE
from stages.play_stage.round_stage.windows.cards_windows.under_mech.tile_cards import TileCards
from stages.play_stage.round_stage.windows.cards_windows.under_mech.inventory_cards import InventoryCards

# TODO
class CardUseArrow:
    def __init__(self, tile_cards: TileCards, inventory: InventoryCards):
        self.tile_cards: TileCards = tile_cards
        self.inventory: InventoryCards = inventory

        self.chosen_card: SkillCard = None

    def update(self):
        if GLOBAL_MOUSE.lmb:
            if self.chosen_card:
                if self.tile_cards.collide(GLOBAL_MOUSE.pos):
                    pass
                elif self.inventory.collide(GLOBAL_MOUSE.pos):
                    card = self.inventory.get_cards_by_mouse_pos(GLOBAL_MOUSE.pos)
                    if self.chosen_card:
                        self.chosen_card.unchoose()

                    self.chosen_card = card

                    if card:
                        card.chose()

                else:
                    self.chosen_card.unchoose()
                    self.chosen_card = None

    def draw(self):
        pass
