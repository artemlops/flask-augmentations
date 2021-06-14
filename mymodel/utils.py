import random


def generate_probabilities(n: int):
    return [random.uniform(0, 1) for _ in range(n)]
