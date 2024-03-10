from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration



from ament_index_python.packages import get_package_share_directory

import os


#Used example it github to structure and write the launch simulation dn navigation simulation 
def generate_launch_description():
	return LaunchDescription([	
		#Launch NavStack 
		#Used this website to help determine how to launch this https://navigation.ros.org/tutorials/docs/navigation2_on_real_turtlebot3.html
		IncludeLaunchDescription(
			PythonLaunchDescriptionSource([
				os.path.join(
					get_package_share_directory('turtlebot3_navigation2'),
					'launch', 'navigation2.launch.py'
				)
			]), 
			launch_arguments={
				'use_sim_time': 'True', 
				'params_file': os.path.join(
					get_package_share_directory('turtlebot3_navigation2'), 
					'/opt/ros/humble/share/nav2_bringup/params/nav2_params.yaml'
				),
				'map': '/home/ryan/ros2_ws_rob599/src/rob599_hw3/resource/map.yaml'
			}.items()
		),
		# Launch Simulation 
		
		IncludeLaunchDescription(
			PythonLaunchDescriptionSource([
				os.path.join(
					get_package_share_directory('turtlebot3_gazebo'),
					'launch/turtlebot3_house.launch.py'
				)
			]),
			launch_arguments={
				'x_pose': '-1.5',
				'y_pose': '1.5'
			}.items()
		),
		 Node(
            #origin: [-6.29, -6.8, 0]
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher_map_odom',
            output='screen',
            arguments=['1.5', '-1.5', '0', '0', '0', '0', 'map', 'odom']
        ),

		
	])