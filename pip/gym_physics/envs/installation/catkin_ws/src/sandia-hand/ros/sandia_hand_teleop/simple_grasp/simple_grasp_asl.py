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
import rospy, sys
from sandia_hand_msgs.srv import SimpleGraspWithSlew
from sandia_hand_msgs.srv import SimpleGraspWithSlewRequest
from sandia_hand_msgs.msg import SimpleGrasp

if __name__ == '__main__':
  if len(sys.argv) != 5:
    print "usage: simple_grasp_asl.py SIDE MESSAGE MOTION_SEC PAUSE_SEC"
    print "  example:  simple_grasp_asl.py only a 2 1"
    sys.exit(1)
  side = sys.argv[1]
  message = sys.argv[2].lower()
  motion_sec = float(sys.argv[3])
  pause_sec = float(sys.argv[4])
  if side == "left":
    side = "left_hand"
  elif side == "right":
    side = "right_hand"
  elif side == "only":
    pass
  else:
    print "side must be 'left' or 'right' or 'only'"
    sys.exit(1)
  if (side == 'only'):
    srv_name = "simple_grasp_with_slew"
  else:
    srv_name = "%s/simple_grasp_with_slew" % side 
  rospy.wait_for_service(srv_name)
  for c in message:
    grasp = "asl_" + c
    if grasp == "asl_ ":
      continue
    print grasp
    try:
      sgs = rospy.ServiceProxy(srv_name, SimpleGraspWithSlew)
      sgs(SimpleGraspWithSlewRequest(SimpleGrasp("asl_" + c, 0), motion_sec))
      rospy.sleep(pause_sec)
    except rospy.ServiceException, e:
      print "service call failed: %s" % e
  sgs(SimpleGraspWithSlewRequest(SimpleGrasp("cylindrical", 0),0)) # return home when done
