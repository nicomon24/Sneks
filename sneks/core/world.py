'''

'''

import numpy as np
import random

class Snek:

    def __init__(self, start_position, start_direction_index=None, start_length=4):
        '''
            DIRECTIONS:
            0: UP (North)
            1: RIGHT (East)
            2: DOWN (South)
            3: LEFT (West)

            ACTIONS:
            0: NOOP
            1: RIGHT
            2: LEFT
        '''
        self.DIRECTIONS = [np.array([-1,0]), np.array([0,1]), np.array([1,0]), np.array([0,-1])]
        self.id = 100
        # Select the start direction
        if start_direction_index is None:
            # Select random direction ()
            self.current_direction_index = np.random.randint(4)
        else:
            self.current_direction_index = start_direction_index
        start_position = start_position
        self.my_blocks = [start_position]
        current_positon = np.array(start_position)
        for i in range(1, start_length):
            # Direction inverse of moving
            current_positon = current_positon - self.DIRECTIONS[self.current_direction_index]
            self.my_blocks.append(tuple(current_positon))

    def step(self, action):
        # Get dAction
        dAction = ((action +1) % 3) - 1
        self.current_direction_index = (self.current_direction_index + dAction) % len(self.DIRECTIONS)
        # Remove tail
        tail = self.my_blocks[-1]
        self.my_blocks = self.my_blocks[:-1]
        # Check new head
        new_head = tuple(np.array(self.my_blocks[0]) + self.DIRECTIONS[self.current_direction_index])
        # Add new head
        self.my_blocks = [new_head] + self.my_blocks
        return new_head, tail

class World:

    def __init__(self, size):
        self.DEAD_REWARD = -100
        self.MOVE_REWARD = -1
        self.EAT_REWARD = 1
        self.FOOD = 1
        # Init a numpy matrix with zeros of predefined size
        self.size = size
        self.world = np.zeros(size)
        # All position list
        self.all_positions = set([(i,j) for i in range(self.size[0]) for j in range(self.size[1])])
        # Init snakes
        self.sneks = [Snek((16,16))]

    def reset(self, n_food=50):
        self.world = np.zeros(self.size)
        # Set N foods
        for i in range(n_food):
            self.place_one_food()

    def place_one_food(self):
        # Get all the available position
        available_positions = self.all_positions
        for snek in self.sneks:
            available_positions = available_positions - set(snek.my_blocks)
        # Choose a place
        choosen_position = random.choice(list(available_positions))
        self.world[choosen_position[0], choosen_position[1]] = self.FOOD

    def get_observation(self):
        obs = self.world.copy()
        # Draw snek over the world
        for snek in self.sneks:
            for block in snek.my_blocks:
                obs[block[0], block[1]] = snek.id
            obs[snek.my_blocks[0][0], snek.my_blocks[0][1]] = snek.id + 1
        return obs

    def move_snek(self, a):
        snek = self.sneks[0]
        new_snek_head, old_snek_tail = snek.step(a)
        # Check if snek is outside bounds
        if not (0 <= new_snek_head[0] < self.size[0]) or not(0 <= new_snek_head[1] < self.size[1]):
            snek.my_blocks = snek.my_blocks[1:]
            return self.get_observation(), self.DEAD_REWARD, True, {}
        # Check if snek eats himself
        if new_snek_head in snek.my_blocks[1:]:
            return self.get_observation(), self.DEAD_REWARD, True, {}
        # Check if snek eats something
        if self.world[new_snek_head[0], new_snek_head[1]] == self.FOOD:
            # Remove old food
            self.world[new_snek_head[0], new_snek_head[1]] = 0
            # Add tail again
            snek.my_blocks.append(old_snek_tail)
            # Place new food
            self.place_one_food()
            reward = self.EAT_REWARD
            # Return
            return self.get_observation(), self.EAT_REWARD, False, {}
        return self.get_observation(), self.MOVE_REWARD, False, {}
