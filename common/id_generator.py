import random


def get_unique_id() -> int:
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1