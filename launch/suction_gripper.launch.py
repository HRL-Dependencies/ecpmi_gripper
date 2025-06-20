#!/usr/bin/env python3
"""
Launch file for ECPMi Suction Gripper Controller

Author: Ehsan Ullah
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ecpmi_gripper',
            executable='suction_gripper_controller',
            name='suction_gripper_controller',
            output='screen',
            parameters=[],
            respawn=True,
            respawn_delay=2.0
        )
    ]) 