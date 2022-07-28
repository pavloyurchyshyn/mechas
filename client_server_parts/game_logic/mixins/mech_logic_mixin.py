from mechas.base.mech import BaseMech
from constants.mechas.detail_const import DetailsTypes
from constants.server.network_keys import ServerResponseCategories, PlayerActions, SRC, PlayerUpdates


class MechLogicMixin:

    def build_players_mechas(self):
        for player in self.players_data.values():
            player.mech = BaseMech(player.start_pos)
            self.logger.info(f'Built mech for {player.token}: {player.mech.__dict__}')
            self.mech_auto_fill(player.mech, player.inventory)

    def update_request_for_players_mechas(self):
        data_to_send = self.data_to_send
        data_to_send[SRC.PlayersUpdates] = data_to_send.get(SRC.PlayersUpdates, {})
        players_updates = data_to_send[SRC.PlayersUpdates]

        for player in self.players_data.values():
            p_update = players_updates[player.token] = players_updates.get(player.token, {})
            p_update[PlayerUpdates.MechData] = self.mech_serializer.mech_to_dict(player.mech)

    def fill_all_mechas(self):
        for player in self.players_data.keys():
            self.player_mech_auto_fill(player)

    def player_mech_auto_fill(self, token):
        mech = self.players_data.get(token).mech
        details = self.players_data.get(token).inventory
        self.mech_auto_fill(mech, details)

    def mech_auto_fill(self, mech: BaseMech, details):
        self.logger.info(f'Fill {mech}: {details}')
        body = list(filter(lambda d: d.detail_type == DetailsTypes.BODY, details))
        if body:
            mech.set_body(body[0])
            details.remove(body[0])

            for detail in details:
                if detail.detail_type == DetailsTypes.BODY:
                    if mech.body is None:
                        mech.set_body(detail)
                else:
                    connected = False
                    for side in (mech.left_slots, mech.right_slots):
                        if connected:
                            break
                        for slot in side.values():
                            if slot.type_is_ok(detail) and slot.is_empty:
                                slot.set_detail(detail)
                                connected = True
                                break
