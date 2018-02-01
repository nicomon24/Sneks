'''
    File to test the environments with an agent taking random actions
'''

import gym
import slither1n
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env', type=str, default='slither1n',
  help="""\
  Blablabla
""")
FLAGS, unparsed = parser.parse_known_args()

env = gym.make(FLAGS.env)

obs = env.reset()
done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()
