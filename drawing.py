import numpy as np
import tensorflow as tf
import gym
from utils import *
import random
import os

class Policy():
    def __init__(self, observation_space, action_space):
        self.observation_space = observation_space
        self.action_space = action_space

        self.observation_size = self.observation_space.shape[0]
        self.action_size = np.prod(self.action_space.shape)
        self.hidden_size = 8

        weight_init = tf.random_uniform_initializer(0, 0)
        bias_init = tf.constant_initializer(0)



        self.obs = tf.placeholder(tf.float32, [None, self.observation_size])
        self.action = tf.placeholder(tf.float32, [None, self.action_size])
        self.advantage = tf.placeholder(tf.float32, [None])
        self.oldaction_dist_mu = tf.placeholder(tf.float32, [None, self.action_size])
        self.oldaction_dist_logstd = tf.placeholder(tf.float32, [None, self.action_size])

        self.policymode = "single"

        if self.policymode == "single":
            with tf.variable_scope("policy"):
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
        elif self.policymode == "multiple":
            action_outputs = []
            action_logstds = []
            for i in xrange(self.action_size):
                with tf.variable_scope("policy"+str(i)):
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
        self.saver = tf.train.Saver()

        self.saver.restore(self.session, tf.train.latest_checkpoint(os.getcwd()+"/training/"))

task = "Reacher-v1"
the_env = gym.make(task)

p = Policy(the_env.observation_space, the_env.action_space)
# saved_policy = np.load("policy.npy")
# for p in saved_policy:
    # print p.shape
# p.set_policy(saved_policy)

ob = filter(the_env.reset())
for x in xrange(100):
    obs = np.expand_dims(ob, 0)
    action_dist_mu, action_dist_logstd = p.session.run([p.action_dist_mu, p.action_dist_logstd], feed_dict={p.obs: obs})
        # samples the guassian distribution
    act = action_dist_mu + np.exp(action_dist_logstd)*np.random.randn(*action_dist_logstd.shape)
    ar = act.ravel()
    print ar
    res = the_env.step(ar)
    ob = filter(res[0])
    the_env.render()
    raw_input(x)
