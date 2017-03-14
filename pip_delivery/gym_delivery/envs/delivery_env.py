import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np

logger = logging.getLogger(__name__)

class DeliveryEnv(gym.Env):
    # metadata = {
    #     'render.modes': ['human', 'rgb_array'],
    #     'video.frames_per_second' : 50
    # }

    def __init__(self, **kwargs):
        # new action space = [left, right]
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(-1, 1, shape=(1,))
        self._seed()
        self.reset()
        self._configure()

        self.n_agents = kwargs.pop('n_agents', 1)

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def _step(self, action):

        for i, a in enumerate(action):
                agent_layer.move_agent(i, a)

        done = is_terminal()

        return np.array(self.state), reward, done, {}

    def _reset(self):
        self.state = np.array((40, 80))

        return self.state

    @property
    def is_terminal(self):
