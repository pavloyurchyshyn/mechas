from visual.cards.base_card import BaseCard
from mechas.base.parts.detail import BaseDetail
from stages.play_stage.round_stage.settings.windows_sizes import RoundSizes

__all__ = ['DetailCard', ]


class DetailCard(BaseCard):
    def __init__(self, detail: BaseDetail,
                 x=RoundSizes.CardSize.X,
                 y=RoundSizes.CardSize.Y,
                 size_x=RoundSizes.CardSize.X_SIZE,
                 size_y=RoundSizes.CardSize.Y_SIZE,
                 ):
        self.detail: BaseDetail = detail
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y,
                         title_text=self.detail.verbal_name,
                         unique_id=detail.unique_id)

    def update(self):
        pass
