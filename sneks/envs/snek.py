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
        - OBS_ZOOM: zoom the observation (only for RGB mode, FIXME)
        - STEP_LIMIT: hard step limit of the environment
        - DYNAMIC_STEP_LIMIT: step limit from the last eaten food (HUNGER)
        - DIE_ON_EAT: set a low difficulty, episode ends after eating the first piece
'''
class SingleSnek(gym.Env):

    metadata = {
        'render.modes': ['human','rgb_array'],
        'observation.types': ['raw', 'rgb']
    }

    def __init__(self, size=(16,16), step_limit=1000, dynamic_step_limit=1000, obs_type='raw', obs_zoom=1, n_food=1, die_on_eat=False, render_zoom=20):
        # Set size of the game world
        self.SIZE = size
        # Set step limit
        self.STEP_LIMIT = step_limit
        # Set dynamic step limit (hunger)
        self.DYNAMIC_STEP_LIMIT = dynamic_step_limit
        self.hunger = 0
        # Set babysnek (dies when eating the first piece)
        self.DIE_ON_EAT = die_on_eat
        # Create world
        self.world = World(self.SIZE, n_sneks=1, n_food=n_food)
        # Set observation type and space
        self.obs_type = obs_type
        if self.obs_type == 'raw':
            self.observation_space = spaces.Box(low=0, high=255, shape=(self.SIZE[0], self.SIZE[1]))
        elif self.obs_type == 'rgb':
            self.observation_space = spaces.Box(low=0, high=255, shape=(self.SIZE[0], self.SIZE[1], 3))
            self.RGBify = RGBifier(self.SIZE, zoom_factor = obs_zoom, players_colors={})
        else:
            raise(Exception('Unrecognized observation mode.'))
        # Action space
        self.action_space = spaces.Discrete(len(self.world.DIRECTIONS))
        # Set renderer
        self.renderer = Renderer(self.SIZE, zoom_factor = render_zoom, players_colors={})

    def _step(self, action):
        # Check if game is ended (raise exception otherwise)
        if not self.alive:
            raise Exception('Need to reset env now.')
        # Check hard and dynamic step limit before performing the action
        self.current_step += 1
        if (self.current_step >= self.STEP_LIMIT) or (self.hunger > self.DYNAMIC_STEP_LIMIT):
            self.alive = False
            return self.world.get_observation(), 0, True, {}
        # Perform the action
        rewards, dones = self.world.move_snek([action])
        # Update and check hunger
        self.hunger += 1
        if rewards[0] > 0:
            self.hunger = 0
        # Check if is a babysnek (dies eating the first piece)
        if rewards[0] > 0 and self.DIE_ON_EAT:
            dones[0] = True
        # Disable interactions if snek has died
        if dones[0]:
            self.alive = False
        return self._get_state(), rewards[0], dones[0], {}

    def _reset(self):
        # Reset step counters
        self.current_step = 0
        self.alive = True
        self.hunger = 0
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
