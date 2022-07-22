from mechas.base.mech import BaseMech
from constants.server.network_keys import PlayerAttrs


class Inventory(list):
    def __init__(self, details=(), length=4):
        self.length = length
        if len(details) > self.length:
            raise ValueError('Too many details')

        super(Inventory, self).__init__(details)

    def append(self, detail) -> None:
        if len(self) < self.length:
            super(Inventory, self).append(detail)
        else:
            raise Exception('Inventory is full')


class Player:
    def __init__(self, token, nickname, number,
                 mech: BaseMech = None, addr=None,
                 is_admin=False, ready=False,
                 inventory: tuple = ()):

        self.addr = addr
        self.nickname = nickname
        self.number = number
        self.token = token
        self.mech: BaseMech = mech
        self.ready: bool = ready
        self.is_admin = is_admin

        self.inventory = Inventory(inventory)
        self.default_details: list = []

    def set_default_details(self, default_details: list):
        self.default_details = default_details

    def get_data_dict(self):
        return {
            PlayerAttrs.Token: self.token,
            PlayerAttrs.Nickname: self.nickname,
            PlayerAttrs.Ready: self.ready,
            PlayerAttrs.IsAdmin: self.is_admin,
            PlayerAttrs.Number: self.number,
        }

    def set_mech(self, mech):
        self.mech = mech

    @property
    def position(self):
        if self.mech:
            return self.mech.position

    @position.setter
    def position(self, position):
        if self.mech:
            self.mech.position = position
