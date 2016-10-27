import gym
import rospy
import os
import signal
import subprocess
import tensorflow as tf
import numpy as np

from gym import utils, spaces
from gym.utils import seeding
from envs import gazebo_env
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

from sensor_msgs.msg import #what sensor are we using? 

class GazeboPointSimpleCameraLocation:

	def __init__(self):
		# Launch the simulation with the given launchfile name
		gazebo_env.GazeboEnv.__init__(self, "GazeboPointSimpleCameraLocation_v0.launch")
        self.vel_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=5)
        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)


        self.action_space = spaces.Discrete(4) #F,L,R,B actions
        self.reward_range = (-np.inf, np.inf)

        self._seed()

    def _seed(self):
    	self.np_random, seed = seeding.np_random(seed)
        return [seed]

	def _step(self, action):
		rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            self.unpause()
        except rospy.ServiceException, e:
            print ("/gazebo/unpause_physics service call failed")

		#Discrete actions
		if action == 0: #FORWARD
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.2
            vel_cmd.angular.z = 0.0
            self.vel_pub.publish(vel_cmd)
        elif action == 1: #LEFT
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.05
            vel_cmd.angular.z = 0.2
            self.vel_pub.publish(vel_cmd)
        elif action == 2: #RIGHT
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.05
            vel_cmd.angular.z = -0.2
            self.vel_pub.publish(vel_cmd)
        elif action == 3: #BACK 
        	vel_cmd = Twist()
            vel_cmd.linear.x = -.02
            vel_cmd.angular.z = 0.0

        data = None
        ''' Need to figure out sensors
        while data is None:   
            try:
                data = rospy.wait_for_message('/scan', LaserScan, timeout=5)
            except:
                pass
		'''
        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            #resp_pause = pause.call()
            self.pause()
        except rospy.ServiceException, e:
            print ("/gazebo/pause_physics service call failed")

        state,done = self.discretize_observation(data,5)

        ''' Need to figure out reward stuff
        if not done:
            if action == 0:
                reward = 5
            else:
                reward = 1
        else:
            reward = -200
		'''
        return state, reward, done, {}



	def _reset(self):

		# Resets the state of the environment and returns an initial observation.
        rospy.wait_for_service('/gazebo/reset_simulation')
        try:
            #reset_proxy.call()
            self.reset_proxy()
        except rospy.ServiceException, e:
            print ("/gazebo/reset_simulation service call failed")

        # Unpause simulation to make observation
        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            #resp_pause = pause.call()
            self.unpause()
        except rospy.ServiceException, e:
            print ("/gazebo/unpause_physics service call failed")

        ''' Sensors 
        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/scan', LaserScan, timeout=5)
            except:
                pass
		'''
        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            #resp_pause = pause.call()
            self.pause()
        except rospy.ServiceException, e:
            print ("/gazebo/pause_physics service call failed")

        state = self.discretize_observation(data,5) 

        return state

	