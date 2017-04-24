import argparse
import logging
import sys
import numpy as np

import gym
from gym import wrappers
import gym_buttons



class RandomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()

if __name__ == '__main__':
    env = gym.make("Hopper-v1")
    # env = gym.wrappers.Monitor(env, "monitor/")

    env.seed(0)
    agent = RandomAgent(env.action_space)

    episode_count = 100
    reward = 0
    done = False

    # env.setgoal = np.array([0.3, 0.0])

    for i in range(episode_count):
        ob = env.reset()
        for x in xrange(100):
            action = agent.act(ob, reward, done)
            action = np.random.uniform(-1, 1, (10,))

            ob, reward, done, _ = env.step(action)
            if done:
                break
            env.render()
