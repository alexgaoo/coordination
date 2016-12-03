import gym
import gym_physics
import numpy as np

env = gym.make("Physics-v0")

for i in xrange(10000):
    env.step(1);
    print i
