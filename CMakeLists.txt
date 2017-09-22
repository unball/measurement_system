cmake_minimum_required(VERSION 2.8.3)
project(measurement_system)

add_message_files(
   FILES
   measurement_msg.msg
)

generate_messages(
   DEPENDENCIES
   std_msgs  # Or other packages containing msgs
)

catkin_package(
  LIBRARIES measurement_system
  CATKIN_DEPENDS vision
  DEPENDS system_lib
)

install(PROGRAMS
   scripts/kalman.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
