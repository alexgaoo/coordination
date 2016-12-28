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

logger = logging.getLogger(__name__)

class ButtonTwoEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
        # new action space = [left, right, up, down]
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(-1, 1, shape=(4,))

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
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        state = self.state
        agent_x, agent_y, goal_x, goal_y = state

        if action == 0:
            agent_x += 1;
        elif action == 1:
            agent_x -= 1;
        elif action == 2:
            agent_y += 1;
        elif action == 3:
            agent_y -= 1;

        self.state = (agent_x, agent_y, goal_x, goal_y)

        done = False

        # reward =  -1 * self._distance(agent_x, agent_y, 90.0, goal_y + 0.0) / 100
        reward = -1 * ((80.0 - agent_x)**2 + (80.0 - agent_y)**2) / 500

        return np.array(self.state), reward, done, {}

    def _reset(self):
        self.state = np.array((40, 40, 80, 80))

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
            self.man_trans = rendering.Transform()
            self.man = rendering.make_circle(10)
            self.man.add_attr(self.man_trans)
            self.goal_trans = rendering.Transform()
            self.goal = rendering.make_circle(10)
            self.goal.add_attr(self.goal_trans)
            self.man.set_color(.5,.5,.8)
            self.viewer.add_geom(self.man)
            self.viewer.add_geom(self.goal)


        agent_x, agent_y, goal_x, goal_y = self.state
        self.man_trans.set_translation(agent_x*4, agent_y*4)
        self.goal_trans.set_translation(goal_x*4, goal_y*4)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')
