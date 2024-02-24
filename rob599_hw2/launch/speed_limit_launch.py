from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rob599_hw2',
            executable='speed_limit',
            name='speed_limit'
        ),
        Node(
            package='rob599_hw2',
            executable='speed_in',
            name='speed_in'
        ),
        Node(
            package='rob599_hw2',
            executable='outside_limit',
            name='outside_limit',
        )
    ])