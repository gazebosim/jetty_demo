cmake_minimum_required(VERSION 3.20)
project(sim_ifaces_demo_assets)

# find dependencies
find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    models/
  DESTINATION share/${PROJECT_NAME}/models
)

install(
  DIRECTORY
    worlds/
  DESTINATION share/${PROJECT_NAME}/worlds
)

ament_package()
