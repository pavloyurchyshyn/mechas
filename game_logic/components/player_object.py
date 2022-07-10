from mechas.base.mech import BaseMech
from constants.network_keys import PlayerAttrs
from constants.mechas.detail_const import MechSerialize


class Player:
    def __init__(self, token, nickname, number, mech: BaseMech = None, addr=None, is_admin=False, ready=False):
        self.addr = addr
        self.nickname = nickname
        self.number = number
        self.token = token
        self.mech: BaseMech = mech
        self.ready: bool = ready
        self.default_details = {}
        self.is_admin = is_admin

    def get_data_dict(self):
        return {
            'token': self.token,
            'nickname': self.nickname,
            'ready': self.ready,
            'is_admin': self.is_admin,
            'number': self.number,
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
