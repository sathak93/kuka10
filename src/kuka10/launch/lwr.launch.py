import os
import launch

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from pathlib import Path
import xacro

def generate_launch_description():
    # TODO(wjwwood): Use a substitution to find share directory once this is implemented in launch
    urdf = os.path.join(get_package_share_directory('kuka10'),'urdf', 'kuka10.urdf'),
    ctrlr_param = os.path.join(get_package_share_directory('kuka10'),'config','fake_controller_config.yaml')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world_file_name = 'workspace'
    urdf_config = xacro.process_file(urdf)
    robot_description = {'robot_description': urdf.toxml()}
    world = os.path.join(get_package_share_directory('kuka10'), 'worlds', world_file_name)
    rviz_config_dir = os.path.join(get_package_share_directory('kuka10'), 'rviz', 'kuka10.rviz')
    return LaunchDescription([
        Node(package='controller_manager', executable='ros2_control_node',parameters=[robot_description, ctrlr_param],
        output={'stdout': 'screen', 'stderr': 'screen',}),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             output='screen', arguments=[urdf]),
        Node(package='rviz2', executable='rviz2', arguments=['-d', rviz_config_dir], output ='screen'),
        Node(package='joint_state_publisher_gui',executable='joint_state_publisher_gui', output='screen')
        #ExecuteProcess(cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so'],output='screen')            
    ])
