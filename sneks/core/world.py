'''

'''

import numpy as np
import random

class Snek:

    '''
        DIRECTIONS:
        0: UP (North)
        1: RIGHT (East)
        2: DOWN (South)
        3: LEFT (West)

        ACTIONS:
        0: UP
        1: RIGHT
        2: DOWN
        3: LEFT
    '''
    DIRECTIONS = [np.array([-1,0]), np.array([0,1]), np.array([1,0]), np.array([0,-1])]

    def __init__(self, snek_id, start_position, start_direction_index, start_length):
        self.snek_id = snek_id
        self.current_direction_index = start_direction_index
        # Place the snek
        start_position = start_position
        self.my_blocks = [start_position]
        current_positon = np.array(start_position)
        for i in range(1, start_length):
            # Direction inverse of moving
            current_positon = current_positon - self.DIRECTIONS[self.current_direction_index]
            self.my_blocks.append(tuple(current_positon))

    def step(self, action):
        # Check if action can be performed (do nothing if in the same direction or opposite)
        if (action != self.current_direction_index) and (action != (self.current_direction_index+2)%len(self.DIRECTIONS)):
            self.current_direction_index = action
        # Remove tail
        tail = self.my_blocks[-1]
        self.my_blocks = self.my_blocks[:-1]
        # Check new head
        new_head = tuple(np.array(self.my_blocks[0]) + self.DIRECTIONS[self.current_direction_index])
        # Add new head
        self.my_blocks = [new_head] + self.my_blocks
        return new_head, tail

class World:

    def __init__(self, size, n_sneks=1, n_food=1):
        self.DEAD_REWARD = -1
        self.MOVE_REWARD = 0
        self.EAT_REWARD = 1
        self.FOOD = 255
        self.DIRECTIONS = Snek.DIRECTIONS
        # Init a numpy matrix with zeros of predefined size
        self.size = size
        self.world = np.zeros(size)
        self.available_positions = set([(i,j) for i in range(self.size[0]) for j in range(self.size[1])])
        # Init sneks
        self.sneks = []
        for _ in range(n_sneks):
            snek = self.register_snek()
            self.available_positions = self.available_positions - set(snek.my_blocks)
        # Set N foods
        for _ in range(n_food):
            self.place_one_food()

    def register_snek(self):
        # Choose position (between [4 and SIZE-4])
        # TODO better choice, no overlap
        SNEK_SIZE = 4
        p = (random.randint(SNEK_SIZE, self.size[0]-SNEK_SIZE), random.randint(SNEK_SIZE, self.size[1]-SNEK_SIZE))
        start_direction_index = random.randrange(len(Snek.DIRECTIONS))
        # Create snek and append
        new_snek = Snek(100 + 2*len(self.sneks), p, start_direction_index, SNEK_SIZE)
        self.sneks.append(new_snek)
        return new_snek

    def place_one_food(self):
        # Choose a place
        choosen_position = random.choice(list(self.available_positions))
        self.world[choosen_position[0], choosen_position[1]] = self.FOOD

    def get_observation(self):
        obs = self.world.copy()
        # Draw snek over the world
        for snek in self.sneks:
            for block in snek.my_blocks:
                obs[block[0], block[1]] = snek.snek_id
            # Highlight head
            obs[snek.my_blocks[0][0], snek.my_blocks[0][1]] = snek.snek_id + 1
        return obs

    # Move the selected snek
    # Returns reward and done flag
    def move_snek(self, actions):
        rewards = []
        dones = []
        for snek, action in zip(self.sneks, actions):
            new_snek_head, old_snek_tail = snek.step(action)
            # Check if snek is outside bounds
            if not (0 <= new_snek_head[0] < self.size[0]) or not(0 <= new_snek_head[1] < self.size[1]):
                snek.my_blocks = snek.my_blocks[1:]
                rewards.append(self.DEAD_REWARD)
                dones.append(True)
                # TODO: remove snek from players
            # Check if snek eats himself
            elif new_snek_head in snek.my_blocks[1:]:
                rewards.append(self.DEAD_REWARD)
                dones.append(True)
                # TODO: remove snek from players
            # Check if snek eats something
            elif self.world[new_snek_head[0], new_snek_head[1]] == self.FOOD:
                # Remove old food
                self.world[new_snek_head[0], new_snek_head[1]] = 0
                # Add tail again
                snek.my_blocks.append(old_snek_tail)
                # Place new food
                self.place_one_food()
                rewards.append(self.EAT_REWARD)
                dones.append(False)
            else:
                rewards.append(self.MOVE_REWARD)
                dones.append(False)
        return rewards, dones
