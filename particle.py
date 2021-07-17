from puzzle import Tile


class Particle:
    def __init__(self,permutation: list[int]) -> None:
        self.permutation = permutation
        self.velocity = 0
        self.p_best = permutation