from mechas.base.mech import BaseMech
from constants.server.network_keys import PlayerAttrs
from constants.mechas.detail_const import MechSerializeConst


class DefaultDetails:
    def __init__(self, body, left_arms, right_arms, left_legs, right_legs):
        self.__body = body
        self.__left_arms = tuple(left_arms)
        self.__right_arms = tuple(right_arms)
        self.__left_legs = tuple(left_legs)
        self.__right_legs = tuple(right_legs)

    @property
    def body(self):
        return self.__body

    @property
    def left_arms(self):
        return self.__left_arms

    @property
    def right_arms(self):
        return self.__right_arms

    @property
    def left_legs(self):
        return self.__left_legs

    @property
    def right_legs(self):
        return self.__right_legs

    def get_dict(self):
        return {
            MechSerializeConst.Body: self.body,
            MechSerializeConst.LeftArms: self.left_arms,
            MechSerializeConst.RightArms: self.right_arms,
            MechSerializeConst.LeftLegs: self.left_legs,
            MechSerializeConst.RightLegs: self.right_legs
        }


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
        self.default_details = {}
        self.is_admin = is_admin

        self.inventory = Inventory(inventory)
        self.default_details: DefaultDetails = None

    def set_default_details(self, body, left_arms, right_arms, left_legs, right_legs):
        self.default_details = DefaultDetails(body, left_arms, right_arms, left_legs, right_legs)

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
