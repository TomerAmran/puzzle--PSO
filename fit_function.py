from random import shuffle
import numpy as np
from utils import load_image

p = 3 / 10
q = 1 / 16


# horizontal disimalerity / horizontal distance
def distance(tile1, tile2):
    K = tile1.shape[0]
    D = tile1.shape[2]  # for RGB should be 3
    pred = 0.0
    for k in range(K):
        for d in range(D):
            predict1 = 2 * tile1[k, K - 1, d] - tile1[k, K - 2, d]
            predict2 = 2 * tile2[k, 0, d] - tile2[k, 1, d]
            pred += (np.abs(predict1 - tile2[k, 0, d]) ** p + \
                     np.abs(predict2 - tile1[k, K - 1, d]) ** p) \
                    ** (q / p)
    return pred


def distance_matrices(tiles: list[any]):
    n = len(tiles)
    H = np.zeros((n, n))
    V = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            H[i, j] = distance(tiles[i], tiles[j])
            V[i, j] = distance(np.transpose(tiles[i], (1, 0, 2)), np.transpose(tiles[j], (1, 0, 2)))
    return H, V


def compability(tiles: list[any]):
    n = len(tiles)
    H, V = distance_matrices(tiles)

    for i in range(n):
        q_h = np.sort(H[i, :])[(n // 4) +1]
        H[i, :] = np.exp(-H[i, :] / q_h)
        H[i, :] /= np.sum(H[i, :])
        q_v = np.sort(V[i, :])[(n // 4)+1]
        V[i, :] = np.exp(-V[i, :] / q_v)
        V[i, :] /= np.sum(V[i, :])
    return H, V
