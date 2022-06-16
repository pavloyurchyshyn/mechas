class NotUniqueId(Exception):
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return f'No unique_id in {self.detail.name}: {self.detail.unique_id}'


class SlotIsFullError(Exception):
    def __init__(self, slot):
        self.slot = slot

    def __str__(self):
        return f'Slot is full: {self.slot.parent}'


class SlotDoesntExistsError(Exception):
    pass


class NotEnoughEnergyError(Exception):
    pass


class SlotClosed(Exception):
    pass


class WrongDetailType(Exception):
    def __init__(self, detail, needed_types):
        self.detail = detail
        self.needed_types = needed_types

    def __str__(self):
        return f'{self.detail.name} has bad detail type, {self.detail.detail_type} not in {self.needed_types}'


class DetailAlreadyConnected(Exception):
    def __init__(self, part, detail):
        self.part = part
        self.detail = detail

    def __str__(self):
        return f'Detail {self.detail} {self.detail.unique_id} already connected to {self.part.name}'


class NoSlotsForMods(Exception):
    def __init__(self, limb):
        self.limb = limb

    def __str__(self):
        return f'No slots for mods in {self.limb.name}'


class NoSlotsForLimbs(Exception):
    def __init__(self, body):
        self.body = body

    def __str__(self):
        return f'No slots in {self.body.name}'
