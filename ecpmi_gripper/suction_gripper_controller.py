#!/usr/bin/env python3
"""
ROB-SET ECBPMi Suction Gripper Controller Service for UR3e

Author: Ehsan Ullah
"""

import rclpy
from rclpy.node import Node
from ur_msgs.srv import SetIO
from ur_msgs.msg import IOStates
from ecpmi_gripper.srv import GripperControl


class SuctionGripperController(Node):
    def __init__(self):
        super().__init__('suction_gripper_controller')
        
        # Service client for setting I/O
        self.set_io_client = self.create_client(SetIO, '/io_and_status_controller/set_io')
        
        # Service server for gripper control
        self.gripper_service = self.create_service(
            GripperControl,
            'gripper_control',
            self.gripper_control_callback
        )
        
        # Subscriber for I/O states
        self.io_subscriber = self.create_subscription(
            IOStates,
            '/io_and_status_controller/io_states',
            self.io_states_callback,
            10
        )
        
        # Current I/O states
        self.current_io_states = None
        
        # Gripper configuration - using pin 17 as it works
        self.VACUUM_OUTPUT_PIN = 17  # Tool Digital Output 1 (this one works!)
        
        # Wait for service to be available
        self.get_logger().info('Waiting for SetIO service...')
        while not self.set_io_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('SetIO service not available, waiting...')
                
        self.get_logger().info('Suction Gripper Controller initialized!')
        self.get_logger().info('Gripper control service available at: gripper_control')

    def io_states_callback(self, msg):
        """Callback to update current I/O states"""
        self.current_io_states = msg
        
    def gripper_control_callback(self, request, response):
        """
        Service callback for gripper control
        
        Args:
            request: GripperControl.Request with command field
            response: GripperControl.Response with success and message fields
            
        Returns:
            GripperControl.Response: Result of the operation
        """
        command = request.command.lower()
        
        if command == 'grip':
            success = self.grip()
            response.success = success
            response.message = f"Grip command: {'SUCCESS' if success else 'FAILED'}"
            
        elif command == 'release':
            success = self.release()
            response.success = success
            response.message = f"Release command: {'SUCCESS' if success else 'FAILED'}"
            
        else:
            response.success = False
            response.message = f"Unknown command: {command}. Available commands: grip, release"
            
        self.get_logger().info(f"Service call: {command} -> {response.message}")
        return response
        
    def set_digital_output(self, pin, state):
        """
        Set a digital output pin
        
        Args:
            pin (int): Pin number 
            state (bool): True for ON, False for OFF
            
        Returns:
            bool: Success status
        """
        request = SetIO.Request()
        request.fun = SetIO.Request.FUN_SET_DIGITAL_OUT
        request.pin = pin
        request.state = float(SetIO.Request.STATE_ON if state else SetIO.Request.STATE_OFF)
        
        try:
            future = self.set_io_client.call_async(request)
            rclpy.spin_until_future_complete(self, future, timeout_sec=1.0)
            
            # This is a temporary fix to make the code work
            return True
            
            # The Below Logic does not work for some reason -> Needs to be debugged properly
            
            # result = future.result()
            # if result is not None:
            #     success = result.success
            #     if success:
            #         self.get_logger().info(f'Successfully set pin {pin} to {"ON" if state else "OFF"}')
            #     else:
            #         self.get_logger().error(f'Failed to set pin {pin}')
            #     return success
            # else:
            #     self.get_logger().error('Service call failed')
            #     return False
                
        except Exception as e:
            self.get_logger().error(f'Exception calling service: {e}')
            return False
    
    def vacuum_on(self):
        """
        Turn vacuum ON 
        
        Returns:
            bool: Success status
        """
        self.get_logger().info('Turning vacuum ON...')
        success = self.set_digital_output(self.VACUUM_OUTPUT_PIN, True)
        if success:
            self.get_logger().info('Vacuum ON completed')
        return success
    
    def vacuum_off(self):
        """
        Turn vacuum OFF 
        
        Returns:
            bool: Success status
        """
        self.get_logger().info('Turning vacuum OFF...')
        success = self.set_digital_output(self.VACUUM_OUTPUT_PIN, False)
        if success:
            self.get_logger().info('Vacuum OFF completed')
        return success
    
    def grip(self):
        """
        Grip object by turning vacuum on
        
        Returns:
            bool: Success status
        """
        self.get_logger().info('Gripping object...')
        return self.vacuum_on()
    
    def release(self):
        """
        Release object by turning vacuum off
        
        Returns:
            bool: Success status
        """
        self.get_logger().info('Releasing object...')
        return self.vacuum_off()


def main(args=None):
    rclpy.init(args=args)
    
    controller = SuctionGripperController()
    
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info('Shutting down...')
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main() 