cmake_minimum_required(VERSION 2.8.3)
project(sandia_hand_description)

find_package(catkin REQUIRED)

# catkin_python_setup()

catkin_package(
)

install(DIRECTORY
  config launch meshes urdf robots
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(FILES
  model.config
  dummy.urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
