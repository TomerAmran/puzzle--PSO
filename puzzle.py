from numpy.random import permutation
import random
from fit_function import compability
from utils import load_image, save_image


class Puzzle:
    def __init__(self, path, tile_size):
        self.tile_size = tile_size
        self.path = path
    def load(self):
        self.tiles, self.h_grid, self.w_grid = load_image(self.path, self.tile_size) 
        self.n = len(self.tiles)
        self.compability_H, self.compability_V = compability(self.tiles)

    def evaluate(self, permutation:list[int]):
        # TODO : refactor to matrix caclulation
        score = 0
        for i in range(self.n):
            if i%self.w_grid != self.w_grid-1:
                score += self.compability_H[permutation[i],permutation[i+1]]
        for j in range(self.w_grid*(self.h_grid-1)):
            score += self.compability_V[permutation[j], permutation[j+self.w_grid]]
        return score
    
    def permutation_to_image(self,path:str,permutation:list[int]):
        tiles = []
        for i in range(self.n):
            tiles.append(self.tiles[permutation[i]])
        return save_image(path,tiles, self.h_grid, self.w_grid)
    
    def ground_trouth_score(self, path, tile_size):
        tiles, h_grid, w_grid = load_image(path, tile_size,shuffle=False) 
        compability_H, compability_V = compability(tiles)
        n = len(tiles)
        permutation = [i for i in range(n)]
        score = 0
        for i in range(n):
            if i%w_grid != w_grid-1:
                score += compability_H[permutation[i],permutation[i+1]]
        for j in range(w_grid*(h_grid-1)):
            score += compability_V[permutation[j], permutation[j+w_grid]]
        return score