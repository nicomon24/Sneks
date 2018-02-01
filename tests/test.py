'''
    File to test the environments with an agent taking random actions
'''

import gym
import sneks
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env', type=str, default='snek-v1',
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
    sleep(1)
