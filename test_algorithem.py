import copy
import random
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
    seed = [i for i in range(puzzle.n)]
    ps = list(all_perms(seed))
    evs = []
    for p in ps:
        evs.append(puzzle.evaluate(p))
    argmin = np.argmin(np.array(evs))
    min = ps[argmin]
    print(argmin,min)
    print(ps)
    return None
def stupid_serach():
    puzzle = Puzzle('imgs/small.jpeg', TILE_SIZE)
    puzzle.load()
    permutations = [puzzle.get_permutation() for _ in range(1000000)]
    scores = [puzzle.evaluate(p) for p in permutations]
    argmax = np.argmax(np.array(scores))
    max_permutation = permutations[argmax]
    puzzle.permutation_to_image('stupid.png',max_permutation)

if (__name__ == '__main__'):
    # exhaustive_search()
    stupid_serach()