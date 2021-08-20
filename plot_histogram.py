import string
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np



def plot_histogram(score_histogram,n_particles,ground_truth,m,n,img_name):
    plt.plot(score_histogram)
    name = img_name + " m:" + str(m) + "n:" + str(n) + " np:" + str(n_particles)  +'\n'+ "ground truth:" + str(ground_truth)
    plt.title(name)
    plt.ylabel(' score')
    plt.xlabel(' iteration')
    plt.savefig("./histograms/" + name + '.png')
    plt.clf()
