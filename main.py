import tensorflow as tf
import numpy as np
import random
import gym
import math
from ops import *

class Agent():
    def __init__(self):
        self.num_observations = 4
        self.num_actions = 2
        self.batchsize = None

    def policy_gradient(self):
        with tf.variable_scope("policy"):
            self.policy_state = tf.placeholder(tf.float32, [self.batchsize, self.num_observations])
            self.policy_actions = tf.placeholder(tf.float32, [self.batchsize, self.num_actions])
            self.policy_advantages = tf.placeholder(tf.float32, [self.batchsize, 1])

            h1 = tf.nn.relu(dense(self.policy_state, self.num_observations, 32, "h1"))
            output = tf.nn.softmax(dense(h1, 32, self.num_actions, "output"))

            # vector of size batchsize
            good_probabilities = tf.reduce_sum(tf.mul(output, self.policy_actions),reduction_indices=[1])
            eligibility = tf.log(good_probabilities) * self.policy_advantages
            loss = -tf.reduce_sum(eligibility)
            self.policy_train = tf.train.AdamOptimizer(0.01).minimize(loss)
            self.policy_eval = output

    def value_function(self):
        with tf.variable_scope("value"):
            self.value_state = tf.placeholder(tf.float32, [self.batchsize, self.num_observations])
            self.value_newvals = tf.placeholder(tf.float32, [self.batchsize, 1])

            h1 = tf.nn.relu(dense(self.value_state, self.num_observations, 32, "h1"))
            output = dense(h1, 32, 1, "output")

            loss = tf.nn.l2_loss(self.value_newvals - output)
            self.value_train = tf.train.AdamOptimizer(0.1).minimize(loss)
            self.value_eval = output

    def train(self):
        self.policy_gradient()
        self.value_function()


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
                probs = self.sess.run(self.policy_eval,feed_dict={self.policy_state: obs_vector})
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

                if done:
                    break

            for index, trans in enumerate(transitions):
                obs, action, reward = trans

                # calculate discounted monte-carlo return
                future_reward = 0
                future_transitions = len(transitions) - index
                decrease = 1
                for index2 in xrange(future_transitions):
                    future_reward += transitions[(index2) + index][2] * decrease
                    decrease = decrease * 0.97
                obs_vector = np.expand_dims(obs, axis=0)
                currentval = self.sess.run(self.value_eval,feed_dict={self.value_state: obs_vector})[0][0]

                # advantage: how much better was this action than normal
                advantages.append(future_reward - currentval)

                # update the value function towards new return
                update_vals.append(future_reward)

            # update value function
            update_vals_vector = np.expand_dims(update_vals, axis=1)
            self.sess.run(self.value_train, feed_dict={self.value_state: states, self.value_newvals: update_vals_vector})
            # real_vl_loss = sess.run(vl_loss, feed_dict={vl_state: states, vl_newvals: update_vals_vector})

            advantages_vector = np.expand_dims(advantages, axis=1)
            self.sess.run(self.policy_train, feed_dict={self.policy_state: states, self.policy_advantages: advantages_vector, self.policy_actions: actions})

            print totalreward

a = Agent()
a.train()
