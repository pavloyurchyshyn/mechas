from mechas.base.parts.detail import BaseDetail
from constants.mechas.detail_const import *


class BaseLeg(BaseDetail):
    is_limb = True
    detail_type = DetailsTypes.LEG_TYPE

    def __init__(self, unique_id, **kwargs):
        super().__init__(unique_id=unique_id, **kwargs)
