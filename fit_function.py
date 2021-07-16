from tile import Tile
from random import shuffle
import numpy as np
from utils import load_image

p = 3/10
q = 1 / 16


# horizontal disimalerity / horizontal distance
def distance(tile1, tile2):
    predict1 = 2*tile1[:,-1] - tile1[:,-2]
    predict2 = 2*tile2[:,0] - tile2[:,1]
    distances =   np.abs(predict1 - tile2[:,0])**p + np.abs(predict2 - tile1[:,-1])**p
    return (distances.sum() ** (q/p))

def distance_matrices(tiles: list[Tile]):
    n = len(tiles)
    H = np.zeros((n,n))
    V = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            H[i,j] = distance(tiles[i].tile, tiles[j].tile)
            V[i,j] = distance(np.transpose(tiles[i].tile,(1,0,2)), np.transpose(tiles[j].tile,(1,0,2)))
    return H, V

def compability(tiles:list[Tile]):
    n = len(tiles)
    H, V = distance_matrices(tiles)
    H , V = -H, -V
    for i in range(n):
        H[i,:] = np.exp(H[i,:]) / np.sum(np.exp(H[i,:]))
        V[i,:] = np.exp(V[i,:]) / np.sum(np.exp(V[i,:]))
    return H,V

