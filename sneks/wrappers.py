"""
    Collection of wrappers for the Sneks environments
"""

import gym
import numpy as np

class NormalizeInt8(gym.ObservationWrapper):

    def __init__(self, env):
        super().__init__(env)
        assert np.max(self.env.observation_space.high) == 255, "Works only for INT8 (255)"
        self.observation_space.high = 1.0
        self.observation_space.dtype = np.dtype(np.float32)

    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        return observation / 255.0, reward, done, info

    def reset(self, **kwargs):
        observation = self.env.reset(**kwargs)
        return observation / 255.0
