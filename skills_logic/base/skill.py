from game_logic.components.steps_clock import StepsClock
from mechas.base.exceptions import SpellWithoutName
from abc import abstractmethod


class BaseSkill:
    """
    Just logic without visual, description etc.
    """
    Clock = StepsClock()
    name = None
    verbal_name = None

    def __init__(self, unique_id: str, spell_cost: int, cooldown: int = 1):
        if self.name is None:
            raise SpellWithoutName

        self.unique_id = f'{unique_id}_{self.name}'

        self.spell_cost = spell_cost
        self.cooldown_value = cooldown
        self.cooldown = 0

    def update_cd(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    @abstractmethod
    def use(self, *args, **kwargs) -> dict:
        raise NotImplementedError

    def on_cooldown(self):
        return self.cooldown_value > 0