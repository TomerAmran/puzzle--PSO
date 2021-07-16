from PIL import Image
import numpy as np
from constants import TILE_SIZE
import random


def load_image(path, shuffle = True):
    img = Image.open(path)
    trimed_height = (img.height // TILE_SIZE) * TILE_SIZE
    trimed_width = (img.width // TILE_SIZE)* TILE_SIZE
    img.crop((0, trimed_height, 0 , trimed_width))

    data = np.array(img) /255

    [grid_width, grid_height] = [trimed_width// TILE_SIZE, trimed_height//TILE_SIZE]

    tiles = [data[i*TILE_SIZE: (i+1)*TILE_SIZE,j*TILE_SIZE: (j+1)*TILE_SIZE] for i in range(grid_height) for j in range(grid_width)]

    if shuffle:
        random.shuffle(tiles)
    
    return tiles , grid_width, grid_height

def save_image(path, tiles, grid_width, grid_height, color_dim=3):
    data = np.zeros((grid_height*TILE_SIZE,grid_width*TILE_SIZE,color_dim))
    print(data.shape)
    k = 0
    for i in range(grid_height):
        for j in range(grid_width):
            data[i*TILE_SIZE: (i+1)*TILE_SIZE,j*TILE_SIZE: (j+1)*TILE_SIZE] =  tiles[k]
            print(data[i*TILE_SIZE: (i+1)*TILE_SIZE,j*TILE_SIZE: (j+1)*TILE_SIZE].shape, tiles[k].shape)
            k += 1
    data = (data * 255).astype(np.uint8)
    img = Image.fromarray(data,'RGB')
    img.save(path)

    


if (__name__ == '__main__'):
    t, w, h =load_image('imgs/small.jpeg')
    save_image('imgs/load_and_save_test.png', t, w, h)