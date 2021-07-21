import numpy as np
from fit_function import compability
from utils import load_image

ts, h, w = load_image('imgs/small.jpeg', tile_size=14, shuffle=False)
H, V = compability(ts)

successes_H = 0

for i in range(len(ts)):
    if np.argmax(H[i, :]) == i + 1:
        if i % w != w - 1:
            successes_H += 1
successes_V = 0
for i in range(len(ts) - w):
    if np.argmax(V[i, :]) == i + w:
        successes_V += 1
score_vertical = successes_V / (w * (h - 1))
score_horizontal = successes_H / ((w - 1) * h)
print('horizontal score', score_horizontal)
print('vertical score', score_vertical)
