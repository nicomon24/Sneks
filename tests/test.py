'''
    File to test the environments with an agent taking random actions
'''

import gym
import sneks
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env', type=str, default=None, help="""Select environment ID.""")
FLAGS, unparsed = parser.parse_known_args()

if FLAGS.env is not None:
    # Creating the environment from its ID
    env = gym.make(FLAGS.env)
else:
    # Creating the environment without gym registering
    from sneks.envs.snek import SingleSnek
    env = SingleSnek(obs_type='rgb', n_food=3)

#env = gym.wrappers.Monitor(env, 'tmp_video')

for e in range(3):
    obs = env.reset()
    print(obs.shape)
    done = False
    r = 0
    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        r += reward
        env.render(mode='human')
        sleep(0.01)

print("Observation:", obs.shape)
env.close()
