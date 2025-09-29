cmake_minimum_required(VERSION 3.22.1 FATAL_ERROR)
project(jetty_demo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# install(DIRECTORY configs DESTINATION share/${PROJECT_NAME})
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
# install(DIRECTORY maps DESTINATION share/${PROJECT_NAME})
install(DIRECTORY worlds DESTINATION share/${PROJECT_NAME})
install(DIRECTORY models DESTINATION share/${PROJECT_NAME})
# install(DIRECTORY rviz DESTINATION share/${PROJECT_NAME})
# install(DIRECTORY params DESTINATION share/${PROJECT_NAME})

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")

# Modified from rmf_demos_maps
# Get absolute path of the building map
set(building_map "maps/jetty_demo/jetty_demo.building.yaml")
get_filename_component(building_map_path ${building_map} REALPATH)

# Get the output world name
string(REGEX REPLACE "\\.[^.]*\.[^.]*$" "" no_extension_path ${building_map_path})
string(REGEX MATCH "[^\/]+$" world_name  ${no_extension_path})

set(output_world_name ${world_name})
set(output_dir ${CMAKE_CURRENT_BINARY_DIR}/maps/${output_world_name})
set(output_world_path ${output_dir}/${output_world_name}.world)
set(output_model_dir ${output_dir}/models)

##############################################################################
# Generate Gz world, download Models, change robot to use Fuel model
##############################################################################

add_custom_command(
  DEPENDS ${building_map_path}
  COMMAND ros2 run rmf_building_map_tools building_map_generator gazebo ${building_map_path} ${output_world_path} ${output_model_dir} --TEMPLATE_WORLD_FILE ${CMAKE_CURRENT_SOURCE_DIR}/worlds/jetty_template.sdf --SKIP_CAMERA_POSE
  OUTPUT ${output_world_path}
)

##############################################################################
# Generate the nav graphs
##############################################################################

set(output_nav_graphs_dir ${output_dir}/nav_graphs/)
set(output_nav_graphs_phony ${output_nav_graphs_dir}/phony)
add_custom_command(
  OUTPUT ${output_nav_graphs_phony}
  COMMAND ros2 run rmf_building_map_tools building_map_generator nav ${building_map_path} ${output_nav_graphs_dir}
  DEPENDS ${building_map_path} ${output_world_path}
)

add_custom_target(generate_${output_world_name}_nav_graphs ALL
  DEPENDS ${output_nav_graphs_phony}
)

install(
  DIRECTORY ${output_dir}
  DESTINATION share/${PROJECT_NAME}/maps
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
