'''

'''

import numpy as np

class Snake:

    def __init__(self, start):
        self.length = 2

class World:

    def __init__(self, size):
        # Init a numpy matrix with zeros of predefined size
        self.size = size
        self.world = np.zeros(size)
        # Init snakes
        self.snakes = []

    def reset(self):
        self.world = np.zeros(size)

    def get_observation(self):
        obs = self.world.copy()
        # Draw snake over the world
        
        #for snek in snakes:

        return obs
