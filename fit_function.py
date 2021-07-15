from random import shuffle
import numpy as np
from load_img import load_image

p = 3/10
q = 1 / 16


# horizontal disimalerity / horizontal distance
def distance(tile1, tile2):
    predict1 = 2*tile1[:,-1] - tile1[:,-2]
    predict2 = 2*tile2[:,0] - tile2[:,1]
    distances =   np.abs(predict1 - tile2[:,0])**p + np.abs(predict2 - tile1[:,-1])**p
    return (distances.sum() ** (q/p))

def fit_matrices(tiles):
    n = len(tiles)
    H = np.zeros((n,n))
    V = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            print(i,j)
            print(distance(tiles[i], tiles[j]))
            H[i,j] = distance(tiles[i], tiles[j])
            V[i,j] = distance(tiles[i].T, tiles[j].T)
    return H, V

if (__name__ == '__main__'):
    ts, h,v = load_image('small.jpeg', shuffle = False)
    for t in ts:
        print(t.shape)
    H,V = fit_matrices(ts)
    print(H)
    