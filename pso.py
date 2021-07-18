from PIL.Image import new
from matplotlib.pyplot import sca
from constants import TILE_SIZE
from utils import SPV, scatter_plot
from puzzle import Puzzle
import random
import numpy as np 
from typing import Callable, Collection
from sklearn.decomposition import PCA as PCA_FACTORY
import time
W = 1
c1 = 0.8
c2 = 0.9
x_min = 0
x_max = 4
v_min = -4
v_max = 4
beta = 0.99


class Particle():
    def __init__(self,dims,fitness: Callable[[list[int]],float]):
        self.dims = dims
        self.position = np.random.rand(dims) * (x_max-x_min) - x_min
        self.pbest_position = self.position
        self.pbest_value = -float('inf')
        self.velocity = np.random.rand(dims) * (v_max-v_min) - v_min
        self.fitness = fitness
    def __str__(self):
        print("I am at ", self.position, " meu pbest is ", self.pbest_position)
    
    def explor1(self,new_position):
        [i,j] = np.random.choice(self.dims,2, replace = False)
        if j<i:
            i,j = j,i
        if j == self.dims-1:
            i, j = 0, i
        new_position[i:j+1] = np.roll(new_position[i:j+1],-1)        
        return new_position
    
    def explor2(self,new_position):
        [i,j] = np.random.choice(self.dims,2)
        new_position[[i,j]] = new_position[[j,i]]
        return new_position
    
    def move(self):
        new_position = self.position + self.velocity
        # new_position /= np.max(new_position)
        new_position = np.clip(new_position, x_min, x_max)
        self.position = new_position
    
    def get_fintness(self):
        return self.fitness(self.position)
    
    # def VNS3(self):
    #     position = self.position
    #     n = self.dims
    #     [i,j] = np.random.choice(n,2, replace = False)
    #     if j<i:
    #         i,j = j,i
    #     if j == self.dims-1:
    #         i, j = 0, i
    #     s = np.copy(position)
    #     s[i:j+1] = np.roll(s[i:j+1],-1) 
    #     loop =0
    #     for k in range((j-i)):
    #             s1 = np.copy(position)
    #             s1[i:k+1] = np.roll(s1[i:k+1],k-j)
    #             if self.fitness(s1) > self.fitness(s):
    #                 s = s1
    #     if self.fitness(s) > self.fitness(position):
    #         self.position = s

    # def VNS2(self):
    #     position = self.position
    #     n = self.dims
    #     for _ in range(10):
    #         s1 = np.copy(position)
    #         indices = (np.random.choice(n,3, replace = False))
    #         indices.sort()
    #         [i,j,k]= indices
    #         s1[i:k+1] = np.roll(s1[i:k+1],k-j)
    #         if self.fitness(s1) > self.position(position)

    def VNS(self):
        position = self.position
        n = self.dims
        [i,j] = np.random.choice(n,2, replace = False)
        if j<i:
            i,j = j,i
        if j == self.dims-1:
            i, j = 0, i
        s = np.copy(position)
        s[i:j+1] = np.roll(s[i:j+1],-1) 
        loop =0
        for _ in range((j-i)):
            kcount =0
            max_method =2
            while True:
                s1 = np.copy(s)
                if kcount == 0:
                    s1[i:j+1] = np.roll(s1[i:j+1],-1)        
                if kcount ==1:
                    s1[[i,j]] = s1[[j,i]]
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
            fitness_cadidate = particle.get_fintness()
            if(fitness_cadidate > particle.pbest_value):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position
            

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = particle.get_fintness()
            if(best_fitness_cadidate > self.gbest_value):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position
    def move_particles(self):
        global W
        W = W*beta if W>0.4 else 0.4
        for i, particle in enumerate(self.particles):
            g_best_candidates = [self.particles[(i-1)].pbest_position, self.particles[(i+1)%self.dims].pbest_position, particle.pbest_position]
            g_best_candidate_values = [self.particles[i-1].pbest_value, self.particles[(i+1)%self.dims].pbest_value, particle.pbest_value]
            g_best = g_best_candidates[np.argmax(g_best_candidate_values)]
            new_velocity = (W*particle.velocity) + (1-W)*(c1*random.random()) * (particle.pbest_position - particle.position) + \
                            (random.random()*c2) * (g_best - particle.position)
            np.clip(new_velocity,v_min, v_max)
            particle.velocity = new_velocity
            particle.move()
            particle.VNS()
    
    


def fitness_1(position: list[int], puzzle:Puzzle):
    permutation = SPV(position)
    return puzzle.evaluate(permutation)


def plot(ps : list[Particle]):
    data = np.array(list(map(lambda p: SPV(p.position),ps)))
    pca = PCA_FACTORY(n_components=2)
    reduced_data = np.array(pca.fit_transform(data))
    scatter_plot(reduced_data.T, np.zeros(len(ps)),1,'scatter')

def main():
    # n_iterations = int(input("Inform the number of iterations: "))
    # n_particles = int(input("Inform the number of particles: "))
    n_iterations = 1000
    n_particles = 200
    puzzle = Puzzle('imgs/small.jpeg',TILE_SIZE//2)
    puzzle.load()
    dims = puzzle.n
    search_space = Space(dims, n_particles)
    fitness = lambda position: fitness_1(position, puzzle)
    particles_vector:list[Particle] = [Particle(dims,fitness) for _ in range(n_particles)]
    search_space.particles = particles_vector

    iteration = 0
    start = time.time()
    while(iteration < n_iterations):
        search_space.set_pbest()    
        search_space.set_gbest()
        print('iteration:{}'.format(iteration),search_space.gbest_value)
        search_space.move_particles()
        # if iteration%1000 == 0:
        #     puzzle.permutation_to_image('imgs/res{}.png'.format(iteration), SPV(search_space.gbest_position))
        iteration += 1
    print('time:', time.time()-start )   
    print("The best solution is: ", search_space.gbest_position)
    puzzle.permutation_to_image('imgs/res.png', SPV(search_space.gbest_position))

if __name__ == '__main__':
    main()
    exit()
    max = 0
    argmax = None
    puzzle = Puzzle('imgs/small.jpeg',TILE_SIZE//2)
    puzzle.load()
    for _ in range(1000000):
        p=Particle(puzzle.n)
        fit = fitness_1(p,puzzle) 
        if fit > max:
            max = fit
            argmax = p
    print(max)
    puzzle.permutation_to_image('serct.png', SPV(argmax.position))

