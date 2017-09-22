cmake_minimum_required(VERSION 2.8.3)
project(measurement_system)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

add_message_files (DIRECTORY msg FILES
  measurement_msg.msg)
generate_messages(DEPENDENCIES std_msgs)

catkin_package(
  CATKIN_DEPENDS
    message_runtime
)

catkin_install_python(PROGRAMS scripts/kalman.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
