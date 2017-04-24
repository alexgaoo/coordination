"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from https://webdocs.cs.ualberta.ca/~sutton/book/code/pole.c
"""

import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from random import randint


logger = logging.getLogger(__name__)

class ButtonTwoEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }



    def __init__(self):
        # new action space = [left, right, up, down]
        self.action_space = spaces.Box(-1.0, 1.0, shape=(2*5,))
        self.observation_space = spaces.Box(-1.0, 1.0, shape=(2*5 + 2*5,))

        self.num_agents = 5
        self.num_goals = 5

        self._seed()
        self.reset()
        self.viewer = None

        self.steps_beyond_done = None

        # Just need to initialize the relevant attributes
        self._configure()

    def _configure(self, display=None):
        self.display = display

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def _step(self, action):

        action = np.tanh(action)

        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        reward = 0
        for i in xrange(self.num_agents):
            self.state[2*i] = self.state[2*i] + action[i]*5
            self.state[2*i + 1] = self.state[2*i + 1] + action[i+1]*5

            individualreward = -1
            for j in xrange(self.num_goals):
                newreward = -1 * ((self.state[self.num_agents*2 + 2*j] - self.state[2*i])**2 + (self.state[self.num_agents*2 + 2*j + 1] - self.state[2*i + 1])**2) / 500
                if individualreward == -1:
                    individualreward = newreward
                elif newreward > individualreward:
                    individualreward = newreward
            reward += individualreward

        done = False

        return self.state, reward, done, {}

    def _reset(self):
        self.state = np.array([])
        for i in xrange(self.num_agents):
            goalpos = [20. + i*30, 20.]
            self.state = np.append(self.state, goalpos)
        for i in xrange(self.num_goals):
            goalpos = [20. + i*30, 80.]
            self.state = np.append(self.state, goalpos)

        return self.state

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        screen_width = 600
        screen_height = 400


        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height, display=self.display)

            self.men = []
            for i in xrange(self.num_agents):
                man_trans = rendering.Transform()
                man = rendering.make_circle(10)
                man.add_attr(man_trans)
                man.set_color(.5,.5,.8)
                self.viewer.add_geom(man)
                self.men.append(man_trans)

            self.goals = []
            for i in xrange(self.num_goals):
                self.goal_trans = rendering.Transform()
                self.goal = rendering.make_circle(10)
                self.goal.add_attr(self.goal_trans)
                self.viewer.add_geom(self.goal)
                self.goals.append(self.goal_trans)


        for i in xrange(self.num_agents):
            self.men[i].set_translation(self.state[2*i]*4, self.state[2*i + 1]*4)

        for i in xrange(self.num_goals):
            self.goals[i].set_translation(self.state[2*self.num_agents + 2*i]*4, self.state[2*self.num_agents + 1 + 2*i]*4)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')
