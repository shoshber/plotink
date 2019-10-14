import random

def get_random_points(num, seed=0):
    """ generate random (but deterministic) points where coords are between 0 and 1 """
    random.seed(seed)

    return [(random.random(), random.random()) for _ in range(num)]
