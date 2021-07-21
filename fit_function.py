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

def distance_matrices(tiles: list[any]):
    n = len(tiles)
    H = np.zeros((n,n))
    V = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            H[i,j] = distance(tiles[i], tiles[j])
            V[i,j] = distance(np.transpose(tiles[i],(1,0,2)), np.transpose(tiles[j],(1,0,2)))
    return H, V

def compability(tiles:list[any]):
    n = len(tiles)
    H, V = distance_matrices(tiles)
   
    for i in range(n):
        q_h = np.quantile(H[i,:], 0.25)
        H[i,:] = np.exp(-H[i,:] / q_h)
        H[i,:] /= np.sum(H[i,:])
        q_v = np.quantile(V[i,:], 0.25)
        V[i,:] = np.exp(-V[i,:]/ q_v)
        V[i,:] /= np.sum(V[i,:])
    return H,V

