cmake_minimum_required(VERSION 2.8.3)
project(sandia_hand_msgs)

find_package(catkin REQUIRED COMPONENTS
  message_generation std_msgs
  )


add_message_files(
  DIRECTORY msg
  FILES
  RelativeJointCommands.msg
  RawTactile.msg
  RawPalmState.msg
  RawMoboState.msg
  RawFingerState.msg
  RawFingerInertial.msg
  Parameter.msg
  CalFingerState.msg
  SimpleGrasp.msg
  RawFingerCommands.msg
  )

add_service_files(DIRECTORY srv FILES
  SimpleGraspSrv.srv
  SimpleGraspWithSlew.srv
  SetParameters.srv
  SetJointLimitPolicy.srv
  SetFingerHome.srv
  GetParameters.srv
  )

generate_messages(DEPENDENCIES
  std_msgs
  )

catkin_package(
  CATKIN_DEPENDS
  message_runtime
  message_generation
  std_msgs
  )
