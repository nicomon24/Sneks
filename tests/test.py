'''
    File to test the environments with an agent taking random actions
'''

import gym
import sneks
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env', type=str, default='babysnek-v1',
  help="""\
  Blablabla
""")
FLAGS, unparsed = parser.parse_known_args()

env = gym.make(FLAGS.env)
#env = gym.wrappers.Monitor(env, 'tmp_video')

obs = env.reset()
done = False
r = 0
while not done:
    action = env.action_space.sample()
    for i in range(2):
        obs, reward, done, info = env.step(action)
        r += reward
        env.render()
        sleep(0.01)
        action = 0
        if done:
            r = 0
            obs = env.reset()
            done = False
