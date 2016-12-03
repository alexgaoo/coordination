# This file allows the developer to skip the step of embedding this repo into a
# catkin workspace (by, e.g., calling catkin_init_workspace).  This repo can
# still be embedded in a catkin workspace, in which case, this file will not be
# processed (because there's no package.xml in this directory).
cmake_minimum_required(VERSION 2.8)
find_package(catkin REQUIRED)
include(${catkin_EXTRAS_DIR}/toplevel.cmake)

project (osrf-common)
include(ExternalProject)
string(REPLACE "-" "_" PROJECT_IDENT ${PROJECT_NAME})
string(TOUPPER ${PROJECT_IDENT} PROJECT_IDENT)

set (OSRF_COMMON_MAJOR_VERSION 1)
set (OSRF_COMMON_MINOR_VERSION 1)
set (OSRF_COMMON_PATCH_VERSION 0)
set (OSRF_COMMON_VERSION ${OSRF_COMMON_MAJOR_VERSION}.${OSRF_COMMON_MINOR_VERSION})
set (OSRF_COMMON_VERSION_FULL ${OSRF_COMMON_MAJOR_VERSION}.${OSRF_COMMON_MINOR_VERSION}.${OSRF_COMMON_PATCH_VERSION})
message (STATUS "${PROJECT_NAME} version ${OSRF_COMMON_VERSION_FULL}")

# Packaging configuration
set (CPACK_PACKAGE_VERSION "${OSRF_COMMON_VERSION_FULL}")
set (CPACK_PACKAGE_VERSION_MAJOR "${OSRF_COMMON_MAJOR_VERSION}")
set (CPACK_PACKAGE_VERSION_MINOR "${OSRF_COMMON_MINOR_VERSION}")
set (CPACK_PACKAGE_VERSION_PATCH "${OSRF_COMMON_PATCH_VERSION}")
list (APPEND CPACK_SOURCE_IGNORE_FILES ";/.hg/;.hgignore;.swp$;/build/")
set (CPACK_SOURCE_PACKAGE_FILE_NAME "@PROJECT_NAME@-@OSRF_COMMON_VERSION_FULL@")
include (CPack)
