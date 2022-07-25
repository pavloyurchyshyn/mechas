import random


class IdGenerator:
    def __init__(self, seed=None):
        self.seed = seed if seed is not None else random.getrandbits(32)

    def set_seed(self, seed):
        self.seed = seed

    def get_id(self):
        seed, self.seed = str(self.seed), self.seed + 1

        return seed

    def __call__(self, *args, **kwargs):
        return self.get_id()


if __name__ == '__main__':
    g = IdGenerator()
