from PIL import Image
import numpy as np
from constants import TILE_SIZE
import random


def load_image(path, shuffle = True):
    img = Image.open(path)
    trimed_height = (img.height // TILE_SIZE) * TILE_SIZE
    trimed_width = (img.width // TILE_SIZE)* TILE_SIZE
    img.crop((0, trimed_height, 0 , trimed_width))

    data = np.array(img) / 255
    [grid_width, grid_height] = [trimed_width// TILE_SIZE, trimed_height//TILE_SIZE]

    tiles = [data[i*TILE_SIZE: (i+1)*TILE_SIZE,j*TILE_SIZE: (j+1)*TILE_SIZE] for i in range(grid_height) for j in range(grid_width)]

    if shuffle:
        random.shuffle(tiles)
    
    return tiles , grid_width, grid_height

if (__name__ == '__main__'):
    t, w, h =load_image('small.jpeg')
    print(w, h)