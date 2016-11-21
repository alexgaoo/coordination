import tensorflow as tf
import numpy as np
import random
import gym
import math
from ops import *

class Agent():
    def __init__(self):
        self.num_observations
        self.num_actions
        self.batchsize

        def policy_gradient():
            with tf.variable_scope("policy"):
                self.policy_state = tf.placeholder(tf.float32, [self.batchsize, self.num_observations])
                self.policy_actions = tf.placeholder(tf.float32, [self.batchsize, self.num_actions])
                self.policy_advantages = tf.placeholder(tf.float32, [self.batchsize, 1])

                h1 = tf.nn.relu(dense(self.policy_state, self.num_observations, 32, "h1"))
                output = tf.nn.softmax(dense(h1, 32, self.num_actions, "output"))

                # vector of size batchsize
                good_probabilities = tf.reduce_sum(tf.mul(probabilities, self.policy_actions),reduction_indices=[1])
                eligibility = tf.log(good_probabilities) * self.policy_advantages
                loss = -tf.reduce_sum(eligibility)
                self.policy_train = tf.train.AdamOptimizer(0.01).minimize(loss)

        def value_function():
            with tf.variable_scope("value"):
                self.value_state = tf.placeholder(tf.float32, [self.batchsize, self.num_observations])
                self.value_newvals = tf.placeholder(tf.float32, [self.batchsize, 1])

                h1 = tf.nn.relu(dense(self.value_state, self.num_observations, 32, "h1"))
                output = tf.nn.softmax(dense(h1, 32, 1, "output"))

                loss = tf.nn.l2_loss(self.value_newvals - output)
                self.value_train = tf.train.AdamOptimizer(0.1).minimize(loss)

        def train():
            env = gym.make('CartPole-v0')
            self.sess = tf.Session();
            self.sess.run(tf.initialize_all_variables())

            for e in xrange(2000):
                observation = env.reset()
                totalreward = 0
                states = []
                actions = []
                advantages = []
                transitions = []
                update_vals = []

                for i in xrange(200):
                    # calculate policy
                    obs_vector = np.expand_dims(observation, axis=0)
                    probs = sess.run(pl_calculated,feed_dict={pl_state: obs_vector})
                    action = 0 if random.uniform(0,1) < probs[0][0] else 1
                    # record the transition
                    states.append(observation)
                    actionblank = np.zeros(2)
                    actionblank[action] = 1
                    actions.append(actionblank)
                    # take the action in the environment
                    old_observation = observation
                    observation, reward, done, info = env.step(action)
                    transitions.append((old_observation, action, reward))
                    totalreward += reward
