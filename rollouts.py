import numpy as np
import tensorflow as tf
import multiprocessing
from utils import *
import gym
import time
import copy
from random import randint

class Actor(multiprocessing.Process):
    def __init__(self, args, task_q, result_q, actor_id, monitor):
        multiprocessing.Process.__init__(self)
        self.task_q = task_q
        self.result_q = result_q
        self.args = args
        self.monitor = monitor

        self.count = 0


    def act(self, obs):
        obs = np.expand_dims(obs, 0)
        action_dist_mu, action_dist_logstd = self.session.run([self.action_dist_mu, self.action_dist_logstd], feed_dict={self.obs: obs})
        # samples the guassian distribution
        act = action_dist_mu + np.exp(action_dist_logstd)*np.random.randn(*action_dist_logstd.shape)

        return act.ravel(), action_dist_mu, action_dist_logstd

    def run(self):

        self.env = gym.make(self.args.task)
        self.env.seed(randint(0,999999))
        # if self.monitor:
            # self.env = gym.wrappers.Monitor(self.env, "monitor/")


        # tensorflow variables (same as in model.py)
        self.observation_size = self.env.observation_space.shape[0]
        self.action_size = np.prod(self.env.action_space.shape)
        self.hidden_size = 8
        weight_init = tf.random_uniform_initializer(-0.05, 0.05)
        bias_init = tf.constant_initializer(0)
        # tensorflow model of the policy
        self.obs = tf.placeholder(tf.float32, [None, self.observation_size])
        self.debug = tf.constant([2,2])

        if self.args.policymode == "single":
            with tf.variable_scope("policy-a"):
                h1 = fully_connected(self.obs, self.observation_size, self.hidden_size, weight_init, bias_init, "policy_h1")
                h1 = tf.nn.relu(h1)
                h2 = fully_connected(h1, self.hidden_size, self.hidden_size, weight_init, bias_init, "policy_h2")
                h2 = tf.nn.relu(h2)
                h3 = fully_connected(h2, self.hidden_size, self.action_size, weight_init, bias_init, "policy_h3")
                action_dist_logstd_param = tf.Variable((.01*np.random.randn(1, self.action_size)).astype(np.float32), name="policy_logstd")
            # means for each action
            self.action_dist_mu = h3
            # log standard deviations for each actions
            self.action_dist_logstd = tf.tile(action_dist_logstd_param, tf.pack((tf.shape(self.action_dist_mu)[0], 1)))
        elif self.args.policymode == "multiple":
            action_outputs = []
            action_logstds = []
            for i in xrange(self.action_size):
                with tf.variable_scope("policy-a"+str(i)):
                    h1 = fully_connected(self.obs, self.observation_size, self.hidden_size, weight_init, bias_init, "policy_h1")
                    h1 = tf.nn.relu(h1)
                    h2 = fully_connected(h1, self.hidden_size, self.hidden_size, weight_init, bias_init, "policy_h2")
                    h2 = tf.nn.relu(h2)
                    h3 = fully_connected(h2, self.hidden_size, 1, weight_init, bias_init, "policy_h3")
                    action_dist_logstd_param = tf.Variable((.01*np.random.randn(1, 1)).astype(np.float32), name="policy_logstd")
                    action_outputs.append(h3)
                    action_logstds.append(action_dist_logstd_param)
                # means for each action
            self.action_dist_mu = tf.concat(1, action_outputs)
                # log standard deviations for each actions
            self.action_dist_logstd = tf.tile(tf.concat(1, action_logstds), tf.pack((tf.shape(self.action_dist_mu)[0], 1)))

        config = tf.ConfigProto(
            device_count = {'GPU': 0}
        )
        self.session = tf.Session(config=config)
        self.session.run(tf.initialize_all_variables())
        var_list = tf.trainable_variables()

        self.set_policy = SetPolicyWeights(self.session, var_list)

        while True:
            # get a task, or wait until it gets one
            next_task = self.task_q.get(block=True)
            if isinstance(next_task, (np.ndarray, np.generic)):
                # discretize
                # print "Setting goal to " + np.array_str(next_task)
                self.env.setgoal = next_task
                path = self.rollout(train=False)
                self.task_q.task_done()
                self.result_q.put(path)
            elif next_task == 1:
                # the task is an actor request to collect experience
                self.env.setgoal = "none"
                path = self.rollout()
                self.task_q.task_done()
                self.result_q.put(path)
            elif next_task == 2:
                print "kill message"
                if self.monitor:
                    self.env.monitor.close()
                self.task_q.task_done()
                break
            elif type(next_task) is list:
                # the task is to set parameters of the actor policy
                self.set_policy(next_task)
                # super hacky method to make sure when we fill the queue with set parameter tasks,
                # an actor doesn't finish updating before the other actors can accept their own tasks.
                time.sleep(0.1)
                self.task_q.task_done()


        return

    def rollout(self, train=True):
        self.count += 1
        obs, actions, rewards, action_dists_mu, action_dists_logstd = [], [], [], [], []
        pob = self.env.reset()
        ob = filter(pob)
        for i in xrange(self.args.max_pathlength - 1):
            if self.monitor and self.count > 600:
                self.env.render()
            if train:
                obs.append(ob)
            else:
                obs.append(pob)
            action, action_dist_mu, action_dist_logstd = self.act(ob)
            actions.append(action)
            action_dists_mu.append(action_dist_mu)
            action_dists_logstd.append(action_dist_logstd)
            res = self.env.step(action)
            pob = res[0]
            ob = filter(res[0])
            rewards.append((res[1]))

            if res[2] or i == self.args.max_pathlength - 2:
                path = {"obs": np.concatenate(np.expand_dims(obs, 0)),
                             "action_dists_mu": np.concatenate(action_dists_mu),
                             "action_dists_logstd": np.concatenate(action_dists_logstd),
                             "rewards": np.array(rewards),
                             "actions":  np.array(actions)}
                # res = self.env.step(action)
                return path
                break

class ParallelRollout():
    def __init__(self, args):
        self.args = args

        self.tasks = multiprocessing.JoinableQueue()
        self.results = multiprocessing.Queue()

        self.actors = []
        self.actors.append(Actor(self.args, self.tasks, self.results, 9999, args.monitor))

        for i in xrange(self.args.num_threads-1):
            self.actors.append(Actor(self.args, self.tasks, self.results, 37*(i+3), False))

        for a in self.actors:
            a.start()

        # we will start by running 20,000 / 1000 = 20 episodes for the first ieration

        self.average_timesteps_in_episode = 1000

    def discretize(self):

        for y in xrange(20):
            for x in xrange(20):
                self.tasks.put(np.array([0.3*(x/20.0), 0.3*(y/20.0)]))
        self.tasks.join()

        paths = []
        for i in xrange(20*20):
            paths.append(self.results.get())

        np.save("disc.npy", np.array(paths))

    def rollout(self):

        # keep 20,000 timesteps per update
        num_rollouts = self.args.timesteps_per_batch / self.average_timesteps_in_episode

        for i in xrange(num_rollouts):
            self.tasks.put(1)

        self.tasks.join()

        paths = []
        while num_rollouts:
            num_rollouts -= 1
            paths.append(self.results.get())

        self.average_timesteps_in_episode = sum([len(path["rewards"]) for path in paths]) / len(paths)
        return paths

    def set_policy_weights(self, parameters):
        for i in xrange(self.args.num_threads):
            self.tasks.put(parameters)
        self.tasks.join()

    def end(self):
        for i in xrange(self.args.num_threads):
            self.tasks.put(2)
