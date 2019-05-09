'''
    File to test the environments with an agent taking random actions
'''

import gym
import sneks
from time import sleep
import argparse

N_SNEKS = 2

parser = argparse.ArgumentParser()
parser.add_argument('--env', type=str, default=None, help="""Select environment ID.""")
FLAGS, unparsed = parser.parse_known_args()

if FLAGS.env is not None:
    # Creating the environment from its ID
    env = gym.make(FLAGS.env)
else:
    # Creating the environment without gym registering
    from sneks.envs.sneks import MultiSneks
    env = MultiSneks(n_sneks= N_SNEKS, size=(24, 24), obs_type='rgb', add_walls=True)

#env = gym.wrappers.Monitor(env, 'tmp_video')

for e in range(3):
    obs = env.reset()
    print(obs.shape)
    dones = [False] * env.N_SNEKS
    r = [0, 0]
    while not all(dones):
        actions = [env.action_space.sample() for _ in range(env.N_SNEKS)]
        obs, rewards, dones, info = env.step(actions)
        r = map(lambda x,y: x+y, zip(r, rewards))
        env.render(mode='human')
        sleep(0.01)

print("Observation:", obs.shape)
env.close()
