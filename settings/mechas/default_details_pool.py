from settings.mechas.details_names import DetailNames
from constants.mechas.detail_const import MechSerializeConst

# detail_name: count of details per player
# when number 1 -> 4 details for 4 players
# 2 -> 8 for 4
# when 0.5 -> 1 detail for 2 players, and 0 for 1
# 0.25 -> 0 for 3, and 1 for 4
# etc

DEFAULT_DETAILS_POOL_SETTINGS = {
    DetailNames.SimpleMetal.Body: 1,
    DetailNames.SimpleMetal.Leg: 2,
    DetailNames.SimpleMetal.Arm: 2,
}

DEFAULT_START_DETAILS = {
    MechSerializeConst.Body: DetailNames.SimpleMetal.Body,
    MechSerializeConst.LeftArms: [(DetailNames.SimpleMetal.Arm, 1), ],
    MechSerializeConst.RightArms: [(DetailNames.SimpleMetal.Arm, 1), ],
    MechSerializeConst.LeftLegs: [(DetailNames.SimpleMetal.Leg, 1), ],
    MechSerializeConst.RightLegs: [(DetailNames.SimpleMetal.Leg, 1), ],
}