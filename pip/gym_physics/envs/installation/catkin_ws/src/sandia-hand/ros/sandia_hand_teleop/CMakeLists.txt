cmake_minimum_required(VERSION 2.8.3)
project(sandia_hand_teleop)

find_package(catkin REQUIRED COMPONENTS osrf_msgs sandia_hand_msgs)

# catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS osrf_msgs sandia_hand_msgs
)

# all install targets should use catkin DESTINATION variables
# See http://ros.org/doc/api/catkin/html/adv_user_guide/variables.html

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
install(PROGRAMS
  nanokontrol/nanokontrol.py
  nanokontrol/nanokontrol_to_jointspace.py
  simple_grasp/simple_grasp.py 
  simple_grasp/simple_grasp_client.py
  data_collection/pull_controller_data.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## Mark other files for installation (e.g. launch and bag files, etc.)
install(FILES
  launch/nanokontrol_simple_grasp.launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
