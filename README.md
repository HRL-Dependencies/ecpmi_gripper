# ECPMi Gripper Package

ROS2 package for controlling the ECPMi suction gripper on the UR3e robot.

## Overview

This package provides a service-based interface for controlling a suction gripper attached to a UR3e robot. It includes:

- A service server that accepts grip/release commands
- A client utility for easy command-line control
- Launch files for easy startup

## Services

### `/gripper_control` (ecpmi_gripper/srv/GripperControl)

**Request:**
- `command` (string): "grip" or "release"

**Response:**
- `success` (bool): True if command executed successfully
- `message` (string): Status message

## Building

```bash
cd suction_gripper_ws
colcon build --packages-select ecpmi_gripper
source install/setup.bash
```

## Usage

### Starting the Service

```bash
# Option 1: Using launch file
ros2 launch ecpmi_gripper suction_gripper.launch.py

# Option 2: Running directly
ros2 run ecpmi_gripper suction_gripper_controller
```

### Using the Client

```bash
# Grip an object
ros2 run ecpmi_gripper gripper_client grip

# Release an object
ros2 run ecpmi_gripper gripper_client release
```

### Using the Service Directly

```bash
# Grip command
ros2 service call /gripper_control ecpmi_gripper/srv/GripperControl "{command: 'grip'}"

# Release command
ros2 service call /gripper_control ecpmi_gripper/srv/GripperControl "{command: 'release'}"
```

## Configuration

The gripper uses digital output pin 17 (Tool Digital Output 1) by default. This can be modified in the `suction_gripper_controller.py` file by changing the `VACUUM_OUTPUT_PIN` variable.

## Dependencies

- rclpy
- ur_msgs
- UR robot driver running with IO controller

## Author

Ehsan Ullah 