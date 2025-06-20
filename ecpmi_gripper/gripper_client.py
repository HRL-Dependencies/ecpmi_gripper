#!/usr/bin/env python3
"""
Client for calling the ECPMi Suction Gripper Controller Service

Author: Ehsan Ullah
"""

import rclpy
from rclpy.node import Node
from ecpmi_gripper.srv import GripperControl
import sys


class GripperClient(Node):
    def __init__(self):
        super().__init__('gripper_client')
        self.client = self.create_client(GripperControl, 'gripper_control')
        
        # Wait for service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Gripper control service not available, waiting...')

    def send_command(self, command):
        """
        Send a command to the gripper service
        
        Args:
            command (str): "grip" or "release"
            
        Returns:
            tuple: (success: bool, message: str)
        """
        request = GripperControl.Request()
        request.command = command
        
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        
        if future.result() is not None:
            response = future.result()
            return response.success, response.message
        else:
            return False, "Service call failed"


def main(args=None):
    rclpy.init(args=args)
    
    client = GripperClient()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ['grip', 'release']:
            success, message = client.send_command(command)
            print(message)
            if not success:
                sys.exit(1)
        else:
            print(f"Unknown command: {command}")
            print("Available commands: grip, release")
            sys.exit(1)
    else:
        print("Usage: ros2 run ecpmi_gripper gripper_client <command>")
        print("Commands: grip, release")
        sys.exit(1)
    
    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main() 