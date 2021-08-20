from os import path
from PIL.Image import new
from matplotlib.pyplot import sca
from utils import SPV, scatter_plot
from puzzle import Puzzle
import random
import numpy as np
from typing import Callable
from sklearn.decomposition import PCA as PCA_FACTORY
import time
from plot_histogram import plot_histogram
W = 1
c1 = 0.8
c2 = 0.9
x_min = 0
x_max = 4
v_min = -1
v_max = 1
beta = 0.999


class Particle:
    def __init__(self, dims, fitness: Callable[[list[int]], float]):
        self.dims = dims
        self.position = np.random.rand(dims) * (x_max - x_min) - x_min
        self.pbest_position = self.position
        self.pbest_value = -float('inf')
        self.velocity = np.random.rand(dims) * (v_max - v_min) - v_min
        self.fitness = fitness

    def __str__(self):
        print("I am at ", self.position, " meu pbest is ", self.pbest_position)

    def move(self):
        new_position = self.position + self.velocity
        new_position = np.clip(new_position, x_min, x_max)
        self.position = new_position

    def get_fitness(self):
        return self.fitness(self.position)

    def VNS(self):
        position = self.position
        n = self.dims
        [i, j] = np.random.choice(n, 2, replace=False)
        if j < i:
            i, j = j, i
        if j == self.dims - 1:
            i, j = 0, i
        s = np.copy(position)
        s[i:j + 1] = np.roll(s[i:j + 1], -1)
        for _ in range((j - i)):
            kcount = 0
            max_method = 2
            while True:
                s1 = np.copy(s)
                if kcount == 0:
                    s1[i:j + 1] = np.roll(s1[i:j + 1], -1)
                if kcount == 1:
                    s1[[i, j]] = s1[[j, i]]
                if self.fitness(s1) > self.fitness(s):
                    kcount = 0
                    s = s1
                else:
                    kcount += 1
                if not kcount < max_method:
                    break
        if self.fitness(s) > self.fitness(position):
            self.position = s


class Space():

    def __init__(self, dims, n_particles):
        self.dims = dims
        self.n_particles = n_particles
        self.particles: list[Particle] = []
        self.gbest_value = -float('inf')
        self.gbest_position = None

    def print_particles(self):
        for particle in self.particles:
            particle.__str__()

    def set_pbest(self):
        for particle in self.particles:
            fitness_cadidate = particle.get_fitness()
            if (fitness_cadidate > particle.pbest_value):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = particle.get_fitness()
            if (best_fitness_cadidate > self.gbest_value):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position

    def move_particles(self):
        global W
        W = max(W*beta, 0.4)
        for i, particle in enumerate(self.particles):
            # g_best_candidates = [self.particles[(i - 1)].pbest_position,
            #                      self.particles[(i + 1) % len(self.particles)].pbest_position, particle.pbest_position]
            # g_best_candidate_values = [self.particles[i - 1].pbest_value,
            #                            self.particles[(i + 1) % len(self.particles)].pbest_value, particle.pbest_value]
            # g_best = g_best_candidates[np.argmax(g_best_candidate_values)]
            new_velocity = (W * particle.velocity) + (c1 * random.random()) * (
                    particle.pbest_position - particle.position) + \
                           (random.random() * c2) * (self.gbest_position - particle.position)
            np.clip(new_velocity, v_min, v_max)
            particle.velocity = new_velocity
            particle.move()
            particle.VNS()

    def replace_week_particle(self):
        argmin = np.argmin([p.get_fitness() for p in  self.particles])
        self.particles[argmin] = Particle(self.dims, self.particles[0].fitness)


def fitness_1(position: list[int], puzzle: Puzzle):
    permutation = SPV(position)
    return puzzle.evaluate(permutation)


def plot(ps: list[Particle]):
    # data = np.array(list(map(lambda p: SPV(p.position),ps)))
    data = np.array(list(map(lambda p: p.position, ps)))
    pca = PCA_FACTORY(n_components=2)
    reduced_data = np.array(pca.fit_transform(data))
    scatter_plot(reduced_data.T, np.zeros(len(ps)), 1, 'scatter')


def main():
    TILE_SIZE = 50
    n_iterations = 500
    n_particles = 200
    img_name = 'shapes3.jpeg'
    PATH = 'imgs/' + img_name
    score_histogram = []

    puzzle = Puzzle(PATH, TILE_SIZE)
    print('main')
    ground_truth = Puzzle.ground_trouth_score(PATH, TILE_SIZE)
    print('ground trouth', ground_truth)
    puzzle.load()
    print('grid size' , 'm:{}, n:{}'.format(puzzle.h_grid,puzzle.w_grid))
    dims = puzzle.n
    search_space = Space(dims, n_particles)
    fitness = lambda position: fitness_1(position, puzzle)
    particles_vector: list[Particle] = [Particle(dims, fitness) for _ in range(n_particles)]
    search_space.particles = particles_vector

    iteration = 0
    print('starting')
    start = time.time()
    while (iteration < n_iterations and search_space.gbest_value < ground_truth):
        search_space.set_pbest()
        search_space.set_gbest()
        print('iteration:{}'.format(iteration), search_space.gbest_value)
        score_histogram.append(search_space.gbest_value)
        search_space.move_particles()
        if ( iteration % 50 ==0):
            for _ in range(20):
                search_space.replace_week_particle()
                
        # search_space.replace_week_particle()
        # search_space.replace_week_particle()
       
        # plot(search_space.particles)
        if iteration%500 == 0:
            puzzle.permutation_to_image('imgs/res{}.png'.format(iteration), SPV(search_space.gbest_position))
        iteration += 1
    plot_histogram(score_histogram,n_particles,ground_truth, puzzle.h_grid,puzzle.w_grid,img_name)

    print('time:', time.time() - start)
    print("The best solution is: ", search_space.gbest_position)
    puzzle.permutation_to_image('imgs/res.png', SPV(search_space.gbest_position))


if __name__ == '__main__':
    main()
