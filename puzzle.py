from fit_function import compability
from tile import Tile
from utils import load_image


class Puzzle:
    def __init__(self, path, TILE_SIZE):
        self.TILE_SIZE = TILE_SIZE
        self.path = path
    def load(self):
        tiles, self.h_grid, self.w_grid = load_image(self.path) 
        self.n = len(tiles)
        self.tiles = [Tile(tile,i) for i,tile in enumerate(tiles) ]
        self.compability_H, self.compability_V = compability(self.tiles)

    def evaluate(self, permutation: list[Tile]):
        score = 0
        for i in range(self.n):
            if i%self.w_grid != self.w_grid-1:
                score += self.compability_H[permutation[i].index,permutation[i+1].index]
        for j in range(self.w_grid*(self.h_grid-1)):
            score += self.compability_V[permutation[j].index, permutation[j+self.w_grid].index]
        return score
