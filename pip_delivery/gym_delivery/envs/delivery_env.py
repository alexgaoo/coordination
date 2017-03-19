# import glob
# import os
# from os.path import join
# from subprocess import call

# import matplotlib.animation as animation
# import matplotlib.pyplot as plt

import numpy as np
import gym
from gym import spaces
from gym.utils import seeding
# from matplotlib.patches import Rectangle


from six.moves import xrange
from utils import agent_utils
from utils.AgentLayer import AgentLayer
from utils.Controllers import RandomPolicy


logger = logging.getLogger(__name__)

class DeliveryEnv(gym.Env, map_pool):
    # metadata = {
    #     'render.modes': ['human', 'rgb_array'],
    #     'video.frames_per_second' : 50
    # }

    def __init__(self, n_agents, obs_range, ):


        self.map_pool = map_pool
        map_matrix = map_pool[0]
        self.map_matrix = map_matrix
        xs, ys = self.map_matrix.shape
        self.xs = xs
        self.ys = ys


        self.n_agents = 1

        self.obs_range = 3  # can see 3 grids around them by default
        #assert self.obs_range % 2 != 0, "obs_range should be odd"
        # self.obs_offset = int((self.obs_range - 1) / 2)

        self.agents = agent_utils.create_agents(self.n_agents, map_matrix, self.obs_range)

        self.agent_layer = AgentLayer(xs, ys, self.agents)


        # self.layer_norm = kwargs.pop('layer_norm', 10)

        # self.n_catch = kwargs.pop('n_catch', 2)

        n_act = self.agent_layer.get_nactions(0)

        self.agent_controller = RandomPolicy(n_act))

        self.current_agent_layer = np.zeros((xs, ys), dtype=np.int32)

        self.delivered = 0.1

        self.all_delivered = 5.0

        # self.include_id = kwargs.pop('include_id', True)

        self.agent_actions = np.zeros(n_act, dtype=np.int32)


        self.low = np.array([0.0 for i in xrange(3 * self.obs_range**2)])
        self.high = np.array([1.0 for i in xrange(3 * self.obs_range**2)])
        # if self.include_id:
        #     self.low = np.append(self.low, 0.0)
        #     self.high = np.append(self.high, 1.0)
        self.action_space = spaces.Discrete(n_act)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4, self.obs_range, self.obs_range))
        # self.local_obs = np.zeros(
        #     (self.n_agents, 4, self.obs_range, self.obs_range))  # Nagents X 3 X xsize X ysize
        self.act_dims = [n_act for i in xrange(self.n_agents)]

        self.model_state = np.zeros((4,) + map_matrix.shape, dtype=np.float32)

        self._seed()
        self.reset()
        self._configure()


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


        return

    @property
    def is_terminal(self):
