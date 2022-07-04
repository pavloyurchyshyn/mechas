from mechas.base.mech import BaseMech
from constants.network_keys import PlayerAttrs
from constants.mechas.detail_const import MechSerialize


class Player:
    def __init__(self, token, player_data: dict, nickname, mech: BaseMech = None, addr=None):
        self.addr = addr
        self.nickname = player_data.get(PlayerAttrs.Nickname) if nickname is None else nickname
        self.token = token
        self.mech: BaseMech = mech
        self.player_data: dict = player_data
        self.ready = False
        self.default_details = {}

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
