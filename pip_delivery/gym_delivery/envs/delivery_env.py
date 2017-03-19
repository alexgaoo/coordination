# import glob
# import os
# from os.path import join
# from subprocess import call

# import matplotlib.animation as animation
# import matplotlib.pyplot as plt

import numpy as np
import gym
from gym import spaces, utils
from gym.utils import seeding
# from matplotlib.patches import Rectangle


from six.moves import xrange
from utils import agent_utils
from utils.AgentLayer import AgentLayer

from random import randint


logger = logging.getLogger(__name__)

class DeliveryEnv(gym.Env):
    # metadata = {
    #     'render.modes': ['human', 'rgb_array'],
    #     'video.frames_per_second' : 50
    # }

    def __init__(self, n_agents, ):

        self.n_agents = 2

        self.agents = agent_utils.create_agents(self.n_agents)

        self.agent_layer = AgentLayer(xs, ys, self.agents)

        n_act = self.agent_layer.get_nactions(0)

        self.current_agent_layer = np.zeros((xs, ys), dtype=np.int32)

        self.delivered = 0.1

        self.all_delivered = 5.0

        # self.include_id = kwargs.pop('include_id', True)

        self.agent_actions = np.zeros(n_act, dtype=np.int32)

        self.action_space = spaces.Discrete(n_act)

        self.observation_space =  #spaces.Box(low=-np.inf, high=np.inf, shape=(4, self.obs_range, self.obs_range))

        self.agents_gone = np.array([False for i in xrange(self.n_agents)])
     
        self.act_dims = [n_act for i in xrange(self.n_agents)]

        self.model_state = np.zeros((4,) + map_matrix.shape, dtype=np.float32)

        self.goals = []
        for i in range(0, 2):
            g = gencoordinates(-50, 50) 
            self.goals.append(next(g))

        self._seed()
        self._reset()



    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def _step(self, action):

        rewards = self.reward()

        for i, a in enumerate(action):
                self.agent_layer.move_agent(i, a)

        obslist = self.collect_obs(self.agent_layer, self.agents_gone)

        agents_delivered = self.remove_agents()

        rewards += self.delivered * agents_delivered

        done = is_terminal()


        return obslist, reward, done, {}

    def _reset(self):
        self.agents_gone.fill(False)

        return self.collect_obs(self.agent_layer, self.agents_gone)


    def reward(self):
    """
    Computes the joint reward  
    """
    # 
    
    rewards = [
            # self.catchr *
            # np.sum(
            #     es[np.clip(self.pursuer_layer.get_position(i)[0] +
            #         self.surround_mask[:,0], 0, self.xs-1),
            #        np.clip(self.pursuer_layer.get_position(i)[1] +
            #         self.surround_mask[:,1], 0, self.ys-1)]
            #        ) 
            # for i in xrange(self.n_pursuers)
    ]
    return np.array(rewards)



    ##########################

    def gencoordinates(m, n):
    seen = set()

    x, y = randint(m, n), randint(m, n)

    while True:
        seen.add((x, y))
        yield (x, y)
        x, y = randint(m, n), randint(m, n)
        while (x, y) in seen:
            x, y = randint(m, n), randint(m, n)

    


    @property
    def is_terminal(self):
        if self.agent_layer.n_agents() == 0:
            return True
        return False

    def collect_obs(self, agent_layer, agent_gone):
        obs = []
        nagent = 0
        for i in xrange(self.n_agents()):
            if agent_gone[i]:
                obs.append(None)
            else:
                o = self.collect_obs_by_idx(agent_layer, nagent)
                obs.append(o)
                nagent += 1
        return obs

    def collect_obs_by_idx(self, agent_layer, agent_idx):


    def remove_agents(self):
        n_removed = 0  
        removed_agents = []


        ai = 0
        for i in xrange(self.n_agents)
            if self.agents_gone[i]:
                continue
            x, y = self.agent_layer.get_position(ai)
            if _distance()  



        for ridx in removed_agents:
            self.agent_layer.remove_agent(ridx)
            n_removed += 1

        return n_removed





