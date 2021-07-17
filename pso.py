from matplotlib.pyplot import sca
from constants import TILE_SIZE
from utils import SPV, scatter_plot
from puzzle import Puzzle
import random
import numpy as np 
from typing import Callable
from sklearn.decomposition import PCA as PCA_FACTORY

W = 1
c1 = 0.8
c2 = 0.9
x_min = 0
x_max = 4
v_min = -4
v_max = 4
beta = 0.9


class Particle():
    def __init__(self,dims):
        self.dims = dims
        self.position = np.random.rand(dims) * (x_max-x_min) - x_min
        self.pbest_position = self.position
        self.pbest_value = -float('inf')
        self.velocity = np.random.rand(dims) * (v_max-v_min) - v_min

    def __str__(self):
        print("I am at ", self.position, " meu pbest is ", self.pbest_position)
    
    def move(self):
        new_position = self.position + self.velocity
        new_position += (np.random.rand(self.dims) - 0.5)*0.2
        new_position = np.clip(new_position, x_min, x_max)

        self.position = new_position
    # def get_permutation():
        

class Space():

    def __init__(self, dims, n_particles, fitness: Callable[[Particle],float]):
        self.dims = dims
        self.n_particles = n_particles
        self.particles: list[Particle] = []
        self.gbest_value = -float('inf')
        self.gbest_position = None
        self.fitness = fitness
    
    def print_particles(self):
        for particle in self.particles:
            particle.__str__()
   
    def set_pbest(self):
        for particle in self.particles:
            fitness_cadidate = self.fitness(particle)
            if(fitness_cadidate > particle.pbest_value):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position
            

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = self.fitness(particle)
            if(best_fitness_cadidate > self.gbest_value):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position

    def move_particles(self):
        for i, particle in enumerate(self.particles):
            global W
            W *= beta
            g_best_candidates = [self.particles[(i-1)].pbest_position, self.particles[(i+1)%self.dims].pbest_position, particle.pbest_position]
            g_best_candidate_values = [self.particles[i-1].pbest_value, self.particles[(i+1)%self.dims].pbest_value, particle.pbest_value]
            g_best = g_best_candidates[np.argmax(g_best_candidate_values)]
            new_velocity = (W*particle.velocity) + (c1*random.random()) * (particle.pbest_position - particle.position) + \
                            (random.random()*c2) * (g_best - particle.position)
            np.clip(new_velocity,v_min, v_max)
            particle.velocity = new_velocity
            particle.move()


def fitness_1(p:Particle, puzzle:Puzzle):
    permutation = SPV(p.position)
    return puzzle.evaluate(permutation)


def plot(ps : list[Particle]):
    data = np.array(list(map(lambda p: p.position,ps)))
    pca = PCA_FACTORY(n_components=2)
    reduced_data = np.array(pca.fit_transform(data))
    scatter_plot(reduced_data.T, np.zeros(len(ps)),1,'scatter')

def main():
    # n_iterations = int(input("Inform the number of iterations: "))
    # n_particles = int(input("Inform the number of particles: "))
    n_iterations = 100
    n_particles = 1000
    puzzle = Puzzle('imgs/small.jpeg',TILE_SIZE//2)
    puzzle.load()
    dims = puzzle.n
    fitness = lambda p: fitness_1(p, puzzle)
    search_space = Space(dims, n_particles,fitness)
    particles_vector:list[Particle] = [Particle(dims) for _ in range(n_particles)]
    search_space.particles = particles_vector

    iteration = 0
    while(iteration < n_iterations):
        search_space.set_pbest()    
        search_space.set_gbest()
        print(search_space.gbest_value)
        search_space.move_particles()
        plot(particles_vector)
        iteration += 1
        
    print("The best solution is: ", search_space.gbest_position)
    puzzle.permutation_to_image('imgs/res.png', SPV(search_space.gbest_position))

if __name__ == '__main__':
    main()
