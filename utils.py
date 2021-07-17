from tile import Tile
from PIL import Image
import numpy as np
import random

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import torch

###
# plot a scatter plot of coordinates with labels labels
# the data contain k classes
###
def scatter_plot(coordinates,labels,k, name):
    fig, ax = plt.subplots()
    for i in range(k):
        idx = labels == i
        data = coordinates[:,idx]
        ax.scatter(data[0],data[1],label=str(i),alpha=0.3,s=10)
    ax.legend(markerscale=2)
    plt.savefig('{}.png'.format(name))


def load_image(path, tile_size=28):
    img = Image.open(path)
    trimed_height = (img.height // tile_size) * tile_size
    trimed_width = (img.width // tile_size)* tile_size
    img.crop((0, trimed_height, 0 , trimed_width))

    data = np.array(img) /255 # normalize RGB

    [grid_width, grid_height] = [trimed_width// tile_size, trimed_height//tile_size]

    tiles = [data[i*tile_size: (i+1)*tile_size,j*tile_size: (j+1)*tile_size] for i in range(grid_height) for j in range(grid_width)]

    return tiles ,grid_height ,grid_width

def save_image(path:str, tiles: list[Tile], grid_height: int,grid_width:int,color_dim:int=3):
    TILE_SIZE = tiles[0].tile.shape[0]
    data = np.zeros((grid_height*TILE_SIZE,grid_width*TILE_SIZE,color_dim))
    k = 0
    for i in range(grid_height):
        for j in range(grid_width):
            data[i*TILE_SIZE: (i+1)*TILE_SIZE,j*TILE_SIZE: (j+1)*TILE_SIZE] =  tiles[k].tile
            k += 1
    data = (data * 255).astype(np.uint8)
    img = Image.fromarray(data,'RGB')
    img.save(path)
    return img
    
def SPV(vector):
    return np.argsort(vector)


if (__name__ == '__main__'):
    t, h, w =load_image('imgs/small.jpeg')
    save_image('imgs/load_and_save_test.png', t, h, w)