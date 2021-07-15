from PIL import Image
import numpy as np
from constants import TILE_SIZE
import random
# sample.png is the name of the image
# file and assuming that it is uploaded
# in the current directory or we need
# to give the path
def load_image(path, shuffle = True):
    img = Image.open(path)
    trimed_height = (img.height // TILE_SIZE) * TILE_SIZE
    trimed_width = (img.width // TILE_SIZE)* TILE_SIZE
    img.crop((0, trimed_height, 0 , trimed_width))

    data = np.array(img)

    [grid_width, grid_height] = [trimed_width// TILE_SIZE, trimed_height//TILE_SIZE]

    tiles = [data[i*TILE_SIZE: (i+1)*TILE_SIZE,j*TILE_SIZE: (j+1)*TILE_SIZE] for i in range(grid_height) for j in range(grid_width)]
    dis = [[[i*TILE_SIZE, (i+1)*TILE_SIZE],[j*TILE_SIZE, (j+1)*TILE_SIZE]] for i in range(grid_width) for j in range(grid_height)]
    # print(dis)
    # print([t.shape for t in tiles])
    # print(len(tiles))
    if shuffle:
        random.shuffle(tiles)
    
    return tiles , grid_width, grid_height

if (__name__ == '__main__'):
    t, w, h =load_image('small.jpeg')
    print(w, h)