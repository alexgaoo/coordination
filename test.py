import gym
import gym_buttons
import numpy as np
import time

env = gym.make("ButtonTwo-v0")
env.monitor.start('monitor/', force=True)

env.reset()
for i in xrange(200):
    observation, reward, done, _ = env.step(2);
    print reward
    time.sleep(0.1);

env.monitor.close()
