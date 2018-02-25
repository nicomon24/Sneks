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
from sneks.core.render import Renderer, RGBifier

'''
    Configurable single snek environment.
    Parameters:
        - SIZE: size of the world (default: 16x16)
        - FOOD: number of foods in the world at a given time (default: 1)
        - OBSERVATION_MODE: return a raw observation (block ids) or RGB observation
'''
class SingleSnek(gym.Env):

    metadata = {
        'render.modes': ['human','rgb_array'],
        'observation.types': ['raw', 'rgb']
    }

    def __init__(self, size=(16,16), step_limit=1000, obs_type='raw', n_food=1):
        # Set size of the game world
        self.SIZE = size
        # Set step limit
        self.STEP_LIMIT = step_limit
        # Create world
        self.world = World(self.SIZE, n_sneks=1, n_food=n_food)
        # Set observation type and space
        self.obs_type = obs_type
        if self.obs_type == 'raw':
            self.observation_space = spaces.Box(low=0, high=255, shape=(self.SIZE[0], self.SIZE[1]))
        elif self.obs_type == 'rgb':
            self.observation_space = spaces.Box(low=0, high=255, shape=(self.SIZE[0], self.SIZE[1], 3))
            self.RGBify = RGBifier(self.SIZE, zoom_factor = 1, players_colors={})
        else:
            raise(Exception('Unrecognized observation mode.'))
        # Action space
        self.action_space = spaces.Discrete(len(self.world.DIRECTIONS))
        # Set renderer
        self.renderer = Renderer(self.SIZE, zoom_factor = 20, players_colors={})

    def _step(self, action):
        self.current_step += 1
        if self.current_step >= self.STEP_LIMIT:
            return self.world.get_observation(), 0, True, {}
        rewards, dones = self.world.move_snek([action])
        return self._get_state(), rewards[0], dones[0], {}

    def _reset(self):
        self.current_step = 0
        # Create world
        self.world = World(self.SIZE, n_sneks=1)
        return self._get_state()

    def _seed(self, seed):
        random.seed(seed)

    def _get_state(self):
        _state = self.world.get_observation()
        if self.obs_type == 'rgb':
            return self.RGBify.get_image(_state)
        else:
            return _state

    def _render(self, mode='human', close=False):
        return self.renderer._render(self.world.get_observation(), mode=mode, close=False)

class SingleBabySnek(SingleSnek):

    def _step(self, action):
        self.current_step += 1
        if self.current_step >= self.STEP_LIMIT:
            return self.world.get_observation(), 0, True, {}
        rewards, dones = self.world.move_snek([action])
        if rewards[0] > 0:
            return self.world.get_observation(), 1, True, {}
        return self.world.get_observation(), rewards[0], dones[0], {}
