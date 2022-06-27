from mechas.base.mech import BaseMech


class Player:
    def __init__(self, token, player_data: dict, mech: BaseMech):
        self.token = token
        self.mech: BaseMech = mech
        self.player_data: dict = player_data
        self.ready = False

    @property
    def position(self):
        return self.mech.position

    @position.setter
    def position(self, position):
        self.mech.position = position
