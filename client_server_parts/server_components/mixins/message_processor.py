from constants.network_keys import ServerResponseCategories, PlayerActions, CheckRegex, SRC


class MessageProcessorMixin:
    def process_messages(self, token, request):
        if PlayerActions.MESSAGE in request:
            message = request.pop(PlayerActions.MESSAGE)
            if message:
                name = self.players_data.get(token).nickname
                message = f'{name}: {message}'
                self.send_bare_message(message)

    def send_bare_message(self, message):
        messages = self.data_to_send.get(ServerResponseCategories.MessagesToAll, [])
        messages.append(message)
        self.data_to_send[ServerResponseCategories.MessagesToAll] = messages