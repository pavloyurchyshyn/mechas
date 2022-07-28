class Scenario:
    def __init__(self, player, actions_count=3):
        self.actions_count = actions_count
        self.player = player

        self.__actions_keys = tuple(range(self.actions_count))
        self.actions = dict.fromkeys(self.__actions_keys)

    def add_action(self, k, action):
        if k not in self.__actions_keys:
            raise IndexError(f'Wrong scenario key "{k}" not in {self.__actions_keys}')

        self.actions[k] = action

    def switch(self, k1, k2):
        self.actions[k1], self.actions[k2] = self.actions[k2], self.actions[k1]

    def reload(self):
        self.actions.clear()

    def get_action(self, k):
        return self.actions.get(k)
