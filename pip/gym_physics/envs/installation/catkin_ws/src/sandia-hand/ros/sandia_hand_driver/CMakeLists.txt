cmake_minimum_required(VERSION 2.8.3)
project(sandia_hand_driver)

find_package(catkin REQUIRED COMPONENTS camera_info_manager image_transport osrf_msgs roscpp sandia_hand_msgs)

# for globally visible python scripts
# catkin_python_setup()

find_package(Boost REQUIRED COMPONENTS system)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES sandia_hand_driver
  CATKIN_DEPENDS camera_info_manager image_transport osrf_msgs roscpp sandia_hand_msgs
#  DEPENDS system_lib
)


include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

#common
add_library(sandia_hand
  common/hand.cpp
  common/finger.cpp
  common/motor_module.cpp
  common/serial_message_processor.cpp
  common/palm.cpp
  common/loose_finger.cpp
  common/lightweightserial.cpp
  common/proximal_phalange.cpp
  common/distal_phalange.cpp
  common/param.cpp
  common/loose_palm.cpp)
target_link_libraries(sandia_hand ${catkin_LIBRARIES})

#cli
add_executable(sandia_hand_cli cli/sandia_hand_cli.cpp)
target_link_libraries(sandia_hand_cli sandia_hand ${catkin_LIBRARIES})

add_executable(loose_finger_cli cli/loose_finger_cli.cpp)
target_link_libraries(loose_finger_cli sandia_hand ${catkin_LIBRARIES})

add_executable(loose_palm_cli cli/loose_palm_cli.cpp)
target_link_libraries(loose_palm_cli sandia_hand ${catkin_LIBRARIES})

add_executable(sandia_hand_firmware_updater cli/firmware_updater.cpp)
target_link_libraries(sandia_hand_firmware_updater sandia_hand ${catkin_LIBRARIES})

install(TARGETS sandia_hand sandia_hand_cli sandia_hand_firmware_updater
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(TARGETS loose_finger_cli
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  RENAME sandia_hand_loose_finger_cli
)

install(TARGETS loose_palm_cli
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  RENAME sandia_hand_loose_palm_cli
)


#nodes
add_executable(sandia_hand_node nodes/sandia_hand_node.cpp)
target_link_libraries(sandia_hand_node sandia_hand ${catkin_LIBRARIES})
set_target_properties(sandia_hand_node PROPERTIES INSTALL_RPATH "${sandia_hand_driver_LIBRARY_DIRS}")
install(TARGETS sandia_hand_node
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

add_executable(sandia_hand_loose_finger_node nodes/sandia_hand_loose_finger_node.cpp)
target_link_libraries(sandia_hand_loose_finger_node sandia_hand ${catkin_LIBRARIES})
set_target_properties(sandia_hand_loose_finger_node PROPERTIES INSTALL_RPATH "${${PKG_NAME}_LIBRARY_DIRS}")
install(TARGETS sandia_hand_loose_finger_node
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

add_executable(sandia_hand_loose_palm_node nodes/sandia_hand_loose_palm_node.cpp)
target_link_libraries(sandia_hand_loose_palm_node sandia_hand ${catkin_LIBRARIES})
set_target_properties(sandia_hand_loose_palm_node PROPERTIES INSTALL_RPATH "${${PKG_NAME}_LIBRARY_DIRS}")
install(TARGETS sandia_hand_loose_palm_node
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


#gui/homing
find_package(Qt4 REQUIRED)
set(sandia_hand_homing_SOURCES gui/homing/main.cpp gui/homing/homing_dialog.cpp)
set(sandia_hand_homing_HEADERS gui/homing/homing_dialog.h)
include(${QT_USE_FILE})
QT4_WRAP_CPP(sandia_hand_homing_HEADERS_MOC ${sandia_hand_homing_HEADERS})
add_definitions(${QT_DEFINITIONS})
add_executable(sandia_hand_homing ${sandia_hand_homing_SOURCES} ${sandia_hand_homing_HEADERS_MOC})
target_link_libraries(sandia_hand_homing ${QT_LIBRARIES} ${catkin_LIBRARIES})
add_dependencies(sandia_hand_homing sandia_hand_msgs_gencpp)
install(TARGETS sandia_hand_homing
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

#gui/maintenance
find_package(Qt4 REQUIRED)
set(sandia_hand_maintenance_SOURCES gui/maintenance/main.cpp gui/maintenance/dialog.cpp)
set(sandia_hand_maintenance_HEADERS gui/maintenance/dialog.h)
QT4_WRAP_CPP(sandia_hand_maintenance_HEADERS_MOC ${sandia_hand_maintenance_HEADERS})
include(${QT_USE_FILE})
add_definitions(${QT_DEFINITIONS})
add_executable(sandia_hand_maintenance ${sandia_hand_maintenance_SOURCES} ${sandia_hand_maintenance_HEADERS_MOC})
target_link_libraries(sandia_hand_maintenance ${QT_LIBRARIES} ${catkin_LIBRARIES})
install(TARGETS sandia_hand_maintenance
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

#gui
install(PROGRAMS
  gui/maintenance.py
  nodes/finger_state_estimator.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY include/sandia_hand_driver/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  FILES_MATCHING PATTERN "*.h"
)

#dynamic reconfigure
# generate_dynamic_reconfigure_options(cfg/Finger.cfg)
# make sure configure headers are built before any node using them
# add_dependencies(example_node ${${PROJECT_NAME}_EXPORTED_TARGETS})

install(FILES
  launch/both_hands.launch
  launch/f2_manufacture_gui.launch
  launch/f3_manufacture_driver.launch
  launch/f3_manufacture_gui.launch
  launch/finger_estimators.launch
  launch/view_both_cams.launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(PROGRAMS
  scripts/f2_init.sh
  scripts/f2_update_all.sh
  scripts/f3_init.sh
  scripts/f3_update_all.sh
  scripts/fmcb_init.sh
  scripts/fmcb_update_all.sh
  scripts/loose_finger_f2burn.sh
  scripts/loose_finger_f3burn.sh
  scripts/loose_finger_mmburn.sh
  scripts/loose_palm_burn.sh
  scripts/mobo_fpga_update.sh
  scripts/mobo_golden_fpga_update.sh
  scripts/mobo_update.sh
  scripts/palm_update.sh
  scripts/start_stereo.sh
  scripts/stereo_frames.txt
  scripts/view_both_cams.sh
  scripts/view_left_cam.sh
  scripts/view_rh_lh_cams.sh
  scripts/view_right_cam.sh
  scripts/view_stereo.sh
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
