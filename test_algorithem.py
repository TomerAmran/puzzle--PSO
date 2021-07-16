import copy
import random
from particle import Particle
from constants import TILE_SIZE
from puzzle import Puzzle
import numpy as np
import itertools
def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                # nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]

def exhaustive_search():
    puzzle = Puzzle('imgs/small.jpeg', TILE_SIZE)
    puzzle.load()
    ps = []
    for _ in range(200):
        t_copy = copy.deepcopy(puzzle.tiles)
        random.shuffle(t_copy)
        ps.append(Particle(t_copy))
    for p in ps:
        print(puzzle.evaluate(p.tiles))
    print(puzzle.evaluate(puzzle.tiles))
    return None
if (__name__ == '__main__'):
    exhaustive_search()
