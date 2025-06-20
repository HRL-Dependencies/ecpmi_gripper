cmake_minimum_required(VERSION 3.8)
project(ecpmi_gripper)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclpy REQUIRED)
find_package(ur_msgs REQUIRED)

# Generate services
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/GripperControl.srv"
  DEPENDENCIES ur_msgs
)

# Install Python executables
install(PROGRAMS
  ecpmi_gripper/suction_gripper_controller.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME suction_gripper_controller
)

install(PROGRAMS
  ecpmi_gripper/gripper_client.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME gripper_client
)

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package() 