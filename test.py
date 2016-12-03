import gym
import gym_physics
import numpy as np

env = gym.make("Physics-v0")

for i in xrange(200):
    env.step(1);
