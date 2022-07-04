from mechas.base.mech import BaseMech
from constants.mechas.detail_const import DetailsAttrs
from mechas.details.simple_metal_parts import MetalArm, MetalLeg, MetalBody


class MetalMech(BaseMech):
    def __init__(self, position):
        body_data = {DetailsAttrs.Id: '0'
                     }
        super(MetalMech, self).__init__(position=position, body_class=MetalBody, body_data=body_data)
        self.body.set_left_arm(0, MetalArm('1'))
        self.body.set_right_arm(0, MetalArm('2'))
        self.body.set_left_leg(0, MetalLeg('3'))
        self.body.set_right_leg(0, MetalLeg('4'))

        self.collect_abilities()
        self.calculate_attrs()
        # print(self.__dict__)


if __name__ == '__main__':
    a = MetalMech((1, 1))
