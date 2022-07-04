import random


class IdGenerator:
    def __init__(self, seed=random.getrandbits(32)):
        self.seed = seed

    def set_seed(self, seed):
        self.seed = seed

    def get_id(self):
        seed, self.seed = str(self.seed), self.seed + 1

        return seed

    def __call__(self, *args, **kwargs):
        return self.get_id()


if __name__ == '__main__':
    g = IdGenerator()
    print(g())
    print(g())
    print(g())
    print(g())
