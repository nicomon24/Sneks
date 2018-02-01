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

from sneks.core.world import World
from sneks.core.render import Renderer

class SingleSnek(gym.Env):

    metadata = {
        'render.modes': ['human']
    }

    def __init__(self):
        self.CHANNELS = 3
        # Set size of the game world
        self.size = (32, 64)
        # Set step limit
        self.step_limit = 200
        # Create world
        self.world = World(self.size)
        # Set observation and action spaces
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.size[0], self.size[1], self.CHANNELS))
        self.action_space = spaces.Discrete(3)
        # Set renderer
        self.renderer = Renderer(self.size, zoom_factor = 10, object_colors={})

    def _step(self, action):
        return self.world.move_snek(action)

    def _reset(self):
        self.current_step = 0
        self.world.reset()
        return self.world.get_observation()

    def _seed(self, seed):
        np.random.seed(seed)

    def _get_state(self):
        return self.world.get_observation()

    def _render(self, mode='human', close=False):
        self.renderer._render(self._get_state(), mode='human', close=False)
