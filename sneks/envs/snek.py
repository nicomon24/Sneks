'''
    Simple single-player snake environment.

    Actions:
    - 0: NOOP, continue in the current direction
    - 1: turn left
    - 2: turn right
'''
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random

from sneks.core.world import World
from sneks.core.render import Renderer

class SingleSnek(gym.Env):

    metadata = {
        'render.modes': ['human','rgb_array']
    }

    def __init__(self):
        # Set size of the game world
        self.SIZE = (16, 16)
        # Set step limit
        self.STEP_LIMIT = 1000
        # Create world
        self.world = World(self.SIZE, n_sneks=1)
        # Set observation and action spaces
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.SIZE[0], self.SIZE[1]))
        self.action_space = spaces.Discrete(len(self.world.DIRECTIONS))
        # Set renderer
        self.renderer = Renderer(self.SIZE, zoom_factor = 20, object_colors={})

    def _step(self, action):
        self.current_step += 1
        if self.current_step >= self.STEP_LIMIT:
            return self.world.get_observation(), 0, True, {}
        rewards, dones = self.world.move_snek([action])
        return self.world.get_observation(), rewards[0], dones[0], {}

    def _reset(self):
        self.current_step = 0
        # Create world
        self.world = World(self.SIZE, n_sneks=1)
        return self.world.get_observation()

    def _seed(self, seed):
        random.seed(seed)

    def _get_state(self):
        return self.world.get_observation()

    def _render(self, mode='human', close=False):
        return self.renderer._render(self._get_state(), mode=mode, close=False)

class SingleBabySnek(SingleSnek):

    def _step(self, action):
        self.current_step += 1
        if self.current_step >= self.STEP_LIMIT:
            return self.world.get_observation(), 0, True, {}
        rewards, dones = self.world.move_snek([action])
        if rewards[0] > 0:
            return self.world.get_observation(), 1, True, {}
        return self.world.get_observation(), rewards[0], dones[0], {}
