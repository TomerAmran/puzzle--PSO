import numpy as np
from fit_function import distance_matrices
from load_img import load_image

ts, w ,h = load_image('small.jpeg', shuffle = False)
H, V = distance_matrices(ts)

successes = 0

for i in range(len(ts)):
    print(i, np.argmin(H[i,:]))
    if np.argmin(H[i,:]) == i+1:
        if i%w != w-1:
            successes += 1

score = successes / ((w-1)*h)
print(score)  

