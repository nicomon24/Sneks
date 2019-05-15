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
        self.alive = True
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

    def __init__(self, size, n_sneks=1, n_food=1, add_walls=False):
        self.DEAD_REWARD = -1.0
        self.MOVE_REWARD = 0.0
        self.EAT_REWARD = 1.0
        self.FOOD = 64
        self.WALL = 255
        self.DIRECTIONS = Snek.DIRECTIONS
        self.add_walls = add_walls
        # Init a numpy matrix with zeros of predefined size
        self.size = size
        self.world = np.zeros(size)
        # Add walls if requested
        if add_walls:
            self.world[0, :] = self.WALL
            self.world[-1, :] = self.WALL
            self.world[:, 0] = self.WALL
            self.world[:, -1] = self.WALL
        # Compute all available_positions for food
        self.base_available_position = set(zip(*np.where(self.world == 0)))
        # Init sneks
        self.sneks = []
        for _ in range(n_sneks):
            snek = self.register_snek()
        # Set N foods
        self.place_food(n_food = n_food)

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

    def get_alive_sneks(self):
        return [snek for snek in self.sneks if snek.alive]

    def place_food(self, n_food=1):
        # Update the available_positions from sneks
        available_positions = self.base_available_position
        for snek in self.get_alive_sneks():
            available_positions = available_positions - set(snek.my_blocks)
        # Place food objects
        for _ in range(n_food):
            # Choose a place
            choosen_position = random.choice(list(available_positions))
            self.world[choosen_position[0], choosen_position[1]] = self.FOOD
            # Remove the current choice for next steps
            available_positions.remove(choosen_position)

    def get_observation(self):
        obs = self.world.copy()
        # Draw snek over the world
        for snek in self.get_alive_sneks():
            for block in snek.my_blocks:
                obs[block[0], block[1]] = snek.snek_id
            # Highlight head
            obs[snek.my_blocks[0][0], snek.my_blocks[0][1]] = snek.snek_id + 1
        return obs

    # Move the selected snek
    # Returns reward and done flag
    def move_snek(self, actions):
        rewards = [0] * len(self.sneks)
        dones = []
        new_food_needed = 0 #Will be used for the food update
        for i, (snek, action) in enumerate(zip(self.sneks, actions)):
            if not snek.alive:
                continue
            new_snek_head, old_snek_tail = snek.step(action)
            # Check if snek is outside bounds
            if not (0 <= new_snek_head[0] < self.size[0]) or not(0 <= new_snek_head[1] < self.size[1]) or self.world[new_snek_head[0], new_snek_head[1]] == self.WALL:
                snek.my_blocks = snek.my_blocks[1:]
                snek.alive = False
            # Check if snek eats himself
            elif new_snek_head in snek.my_blocks[1:]:
                snek.alive = False
            # Check if snek is eating another snek
            for j, other_snek in enumerate(self.sneks):
                if i != j and other_snek.alive:
                    # Check if heads collided
                    if new_snek_head == other_snek.my_blocks[0]:
                        snek.alive = False
                        other_snek.alive = False
                    # Check head collided with another snek body
                    elif new_snek_head in other_snek.my_blocks[1:]:
                        snek.alive = False
            # Check if snek eats something
            if snek.alive and self.world[new_snek_head[0], new_snek_head[1]] == self.FOOD:
                # Remove old food
                self.world[new_snek_head[0], new_snek_head[1]] = 0
                # Add tail again
                snek.my_blocks.append(old_snek_tail)
                # Request to place new food. New food creation cannot be called here directly, need to update all sneks before
                new_food_needed = new_food_needed + 1
                rewards[i] = self.EAT_REWARD
            elif snek.alive:
                # Didn't eat anything, move reward
                rewards[i] = self.MOVE_REWARD
        # Compute done flags and assign dead rewards
        dones = [not snek.alive for snek in self.sneks]
        rewards = [r if snek.alive else self.DEAD_REWARD for r, snek in zip(rewards, self.sneks)]
		#Adding new food.
        if new_food_needed > 0:
            self.place_food(n_food = new_food_needed)
        return rewards, dones
