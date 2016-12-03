#!/usr/bin/env python
#
# Software License Agreement (Apache License)
#
# Copyright 2013 Open Source Robotics Foundation
# Author: Morgan Quigley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import roslib; roslib.load_manifest('sandia_hand_teleop')
import rospy
import sys
from sandia_hand_msgs.srv import SimpleGraspSrv, SimpleGraspSrvResponse, SimpleGraspWithSlew, SimpleGraspWithSlewResponse
from sandia_hand_msgs.msg import SimpleGrasp
from osrf_msgs.msg import JointCommands

g_jc_pub = None
g_jc = JointCommands()
g_prev_jc_target = JointCommands()

def grasp_srv(req):
  grasp_cb(req.grasp)
  return SimpleGraspSrvResponse()

def grasp_slew_srv(req):
  #print "going to %s in %.3f" % (req.grasp.name, req.slew_duration)
  rate = rospy.Rate(100.0)
  t_start = rospy.Time.now()
  t_end = t_start + rospy.Duration(req.slew_duration)
  while rospy.Time.now() < t_end:
    dt = (rospy.Time.now() - t_start).to_sec()
    dt_norm = dt / req.slew_duration
    #print "%.3f" % dt_norm
    grasp_spline(req.grasp.name, req.grasp.closed_amount, dt_norm)
    rate.sleep()
  grasp_spline(req.grasp.name, req.grasp.closed_amount, 1.0)
  return SimpleGraspWithSlewResponse()

def grasp_spline(grasp_name, closed_amount, spline_amount):
  global g_jc_pub, g_jc, g_prev_jc_target
  #print "request: grasp [%s] amount [%f]" % (grasp_name, closed_amount)
  # save some typing
  gn = grasp_name
  x = closed_amount
  if x < 0:
    x = 0
  elif x > 1:
    x = 1
  origin = [0] * 12
  g0 = [0] * 12
  if (gn == "cylindrical"):
    g0 = [0,1.5,1.7, 0,1.5,1.7, 0,1.5,1.7, 0.2,.8,1.2]
  elif (gn == "spherical"):
    origin = [-0.7,0,0, 0.1,0,0, 0.7,0,0, 0,0,0]
    g0 = [0,1.4,1.4, 0,1.4,1.4, 0,1.4,1.4, 0,0.7,0.7]
  elif (gn == "prismatic"):
    origin = [0,1.4,0, 0,1.4,0, 0,1.4,0, -0.1,0.8,-0.8]
    g0 = [0,0,1.4, 0,0,1.4, 0,0,1.4, 0,0,1.4]
  elif (gn == "finger_0_test"):
    g0 = [0,1.5,1.7, 0,0,0, 0,0,0, 0,0,0]
  elif (gn == "number_one"):
    origin = [0,0,0,  0,1.5,1.5, 0,1.5,1.5, 0.4,0.8,1 ]
  elif (gn == "peace"):
    origin = [-0.2,0,0,  0.05,0,0, 0,1.5,1.5, 0.4,0.8,1 ]
  elif (gn == "asl_a"):
    origin = [0,1.5,1.5,  0,1.5,1.5, 0,1.5,1.5, 1.5,0.9,0.2 ]
  elif (gn == "asl_b"):
    origin = [0.1,0,0,  0,0,0, -0.1,0,0, 1,0.8,0.9 ]
  elif (gn == "asl_c"):
    origin = [0,0.7,0.9, 0,0.7,0.9, 0,0.7,0.9, 0,0.4,0.4 ]
  elif (gn == "asl_d"):
    origin = [0,0,0,  0,1.5,1.5, 0,1.5,1.5, 0.4,0.8,1 ]
  elif (gn == "asl_e"):
    origin = [0,1,1.8, 0,1,1.8, 0,1,1.8, 1.5,0.6,1]
  elif (gn == "asl_f"):
    origin = [0,1.3,1.2, 0.1,0,0, 0.2,0,0, 0.3,0.7,0.7 ]
  elif (gn == "asl_g"):
    origin = [0,1.5,0, 0,1.5,1.5, 0,1.5,1.5, 0,1,-.4 ]
  elif (gn == "asl_h"):
    origin = [0.1,1.5,0, 0,1.5,0, 0,1.5,1.5, 0,1,0.6 ]
  elif (gn == "asl_i"):
    origin = [0,1.5,1.5,  0,1.5,1.5, 0,0,0, 1.5,1.0,0.3 ]
  elif (gn == "asl_j"):
    origin = [0,1.5,1.5,  0,1.5,1.5, 0,0,0, 1.5,1.0,0.3 ]
    g0 = [0,0,0, 0,0,0, 0,0,0, 0.5,1,1]
    g1 = [0,0,0, 0,0,0, 0,0,0, 0,1,1]
  elif (gn == "asl_k"):
    origin = [0,0,0, 0,1.5,0, 0,1.5,1.5, 1.5,1.0,0.3]
  elif (gn == "asl_l"):
    origin = [0,0,0, 0,1.5,1.5, 0,1.5,1.5, 1.5,0,0]
  elif (gn == "asl_m"):
    origin = [0,1,1.5, 0,1,1.5, 0,1,1.5, 0,1,1]
  elif (gn == "asl_n"):
    origin = [0,1,1.5, 0,1,1.5, 0,1.5,1.5, 0,1,1]
  elif (gn == "asl_o"):
    origin = [0.1,1.3,1.2, 0,1.3,1.2, -0.1,1.3,1.2, 0.2,0.8,0.5]
  elif (gn == "asl_p"):
    origin = [0,0,0, 0,1.5,0, 0,1.5,1.5, 1.5,1,0.3]
  elif (gn == "asl_q"):
    origin = [0,1.3,1.2, 0,1.5,1.5, 0,1.5,1.5, 0.4,0.8,0.5]
  elif (gn == "asl_r"):
    origin = [0.1,0,0, -0.1,0,0, 0,1.5,1.5, 0,1,1]
  elif (gn == "asl_s"):
    origin = [0,1.5,1.5, 0,1.5,1.5, 0,1.5,1.5, 0,1,0.2]
  elif (gn == "asl_t"):
    origin = [-.4,1.3,1.5, 0,1.5,1.5, 0,1.5,1.5, 0.4,1,1]
  elif (gn == "asl_u"):
    origin = [0,0,0, 0,0,0, 0,1.5,1.5, 0,1,1]
  elif (gn == "asl_v"):
    origin = [-0.3,0,0, 0.1,0,0, 0,1.5,1.5, 0,1,1]
  elif (gn == "asl_w"):
    origin = [-0.3,0,0, 0,0,0, 0.3,0,0, 0,1,1]
  elif (gn == "asl_x"):
    origin = [0,0,1.5, 0,1.5,1.5, 0,1.5,1.5, 0,1,1]
  elif (gn == "asl_y"):
    origin = [0,1.5,1.5, 0,1.5,1.5, 0.3,0,0, 1.5,0,0]
  elif (gn == "asl_z"):
    origin = [0,1.0,0, 0,1.5,1.5, 0,1.5,1.5, 0.4,0.8,0.8]
    g0 = [0.3,0.3,0, 0,0,0, 0,0,0, 0,0,0]
    g1 = [-0.3,0.3,0, 0,0,0, 0,0,0, 0,0,0]
  else:
    return None # bogus
  g_jc.position = [0] * 12
  if (spline_amount < 0):
    spline_amount = 0
  elif (spline_amount > 1):
    spline_amount = 1
  for i in xrange(0, 12):
    target = origin[i] + g0[i] * x
    prev_target = g_prev_jc_target.position[i]
    #g_jc.position[i] = origin[i] + g0[i] * x
    #delta = target - g_prev_jc_target.position[i]
    # compute convex combination between old and new targets
    g_jc.position[i] = (      spline_amount) * target +  \
                       (1.0 - spline_amount) * prev_target
  #print "joint state: %s" % (str(g_jc.position))
  g_jc_pub.publish(g_jc)
  if (spline_amount == 1.0):
    for i in xrange(0, 12):
      g_prev_jc_target.position[i] = g_jc.position[i] # todo: make this better

def grasp_cb(msg):
  grasp_spline(msg.name, msg.closed_amount, 1)

if __name__ == '__main__':
  rospy.init_node('simple_grasp')
  g_jc.name = ["f0_j0", "f0_j1", "f0_j2",
               "f1_j0", "f1_j1", "f1_j2",
               "f2_j0", "f2_j1", "f2_j2",
               "f3_j0", "f3_j1", "f3_j2"]
  g_jc.position = [0] * 12
  g_prev_jc_target.position = [0] * 12
  g_jc_pub = rospy.Publisher('joint_commands', JointCommands, queue_size=1) # same namespace
  g_jc_srv = rospy.Service('simple_grasp', SimpleGraspSrv, grasp_srv)
  g_sgws_srv = rospy.Service('simple_grasp_with_slew', SimpleGraspWithSlew, grasp_slew_srv)
  g_jc_sub = rospy.Subscriber('simple_grasp', SimpleGrasp, grasp_cb)
  print "simple grasp service is now running."
  rospy.spin()
