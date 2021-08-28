import string
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np



def plot_histogram(score_histogram,n_particles,ground_truth,m,n,elapsed_time,img_name):
    number_of_pices = m*n
    plt.plot(score_histogram)
    plt.plot(np.ones(len(score_histogram))*ground_truth)
    plt.legend(['histogram score','target score'], loc='upper left')
    name = img_name + " pieces: " + str(number_of_pices) + " np:" + str(n_particles)  +'\n'+ "ground truth:" + str(ground_truth) + ' time:' +str(elapsed_time)
    plt.title(name)
    plt.ylabel(' score')
    plt.xlabel(' iteration')
    plt.savefig("./histograms/" + name + '.png')
    plt.clf()
