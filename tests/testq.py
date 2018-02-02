'''
    File to test the environments with an agent taking random actions
'''

import gym
import sneks
from time import sleep
import argparse
import numpy as np
from tqdm import trange
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--env', type=str, default='snek-v1',
  help="""\
  Blablabla
""")
FLAGS, unparsed = parser.parse_known_args()

env = gym.make(FLAGS.env)

def extract_head_food(observation):
    head = np.where(observation == 101)
    head = (head[0][0], head[1][0])
    body1 = np.where(observation == 102)
    body1 = (body1[0][0], body1[1][0])
    food = np.where(observation == 1)
    if len(food[0]) > 0:
        food = (food[0][0], food[1][0])
    else:
        food = (0,0)
    return (head[0], head[1], body1[0], body1[1], food[0], food[1])

Q = np.zeros((32, 32, 32, 32, 32, 32, env.action_space.n))
LEARNING_RATE = 0.2
DISCOUNT_FACTOR = 0.99
EPSILON = 0.5

N_EPISODES_TRAIN = 100000
N_EPISODES_TOTAL = N_EPISODES_TRAIN + 100

env.seed(0)

DEBUG_PACE = 10000

for episode in trange(N_EPISODES_TOTAL):
    # Play one episode and updated
    obs = env.reset()
    state = extract_head_food(obs)
    done = False
    steps = 0
    maxQ_sum = 0
    while not done:
        _previous_state = state
        # Choose the action
        if np.random.random() < (EPSILON * (1 - episode / N_EPISODES_TOTAL)):
            # Choose a random action for epsilon-greedy
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state[0],state[1],state[2],state[3],state[4],state[5],:])
        maxQ_sum += max(Q[state[0],state[1],state[2],state[3],state[4],state[5],:])
        steps += 1
        obs, reward, done, info = env.step(action)
        state = extract_head_food(obs)
        # Update Q function
        Q[_previous_state[0],_previous_state[1],
            _previous_state[2], _previous_state[3],
            _previous_state[4], _previous_state[5], action] = (1-LEARNING_RATE) *\
                Q[_previous_state[0],_previous_state[1],
                  _previous_state[2],_previous_state[3],
                  _previous_state[4],_previous_state[5], action] +\
                LEARNING_RATE * (reward + DISCOUNT_FACTOR * max(Q[state[0],state[1],
                                                                  state[2],state[3],
                                                                  state[4],state[5],:]))
        if episode > N_EPISODES_TRAIN or episode % DEBUG_PACE == 0:
            env.render()
            sleep(0.05)
    # Print some debug info
    mean_maxQ = maxQ_sum / steps
    print("Episode:", episode," - Total steps:", steps," - Mean max Q:", mean_maxQ)
    if episode % DEBUG_PACE == 0:
        # Plot Q matrix
        Q_fooded = Q[:,:,:,:,_previous_state[4],_previous_state[5],:]
        Qmax = np.amax(Q_fooded, axis=(2,3,4))
        cv2.imwrite("Qmax_" + str(episode) +".png", Qmax)
