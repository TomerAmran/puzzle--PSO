import copy
import random
from particle import Particle
from constants import TILE_SIZE
from puzzle import Puzzle
import numpy as np


def exhaustive_search():
    puzzle = Puzzle('imgs/small.jpeg', TILE_SIZE)
    puzzle.load()
    ps = []
    for _ in range(10):
        t_copy = copy.deepcopy(puzzle.tiles)
        random.shuffle(t_copy)
        ps.append(Particle(t_copy))
    for p in ps:
        print(puzzle.evaluate(p.tiles))
    print(puzzle.evaluate(puzzle.tiles))
    return None
if (__name__ == '__main__'):
    exhaustive_search()
