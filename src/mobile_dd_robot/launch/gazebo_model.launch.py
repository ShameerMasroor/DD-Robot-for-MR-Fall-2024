import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import  PythonLaunchDescriptionSource

from launch_ros.actions import Node
import xacro


def generate_launch_description():
    # This name has to match the robot name in the Xacro file
    robotXacroName = 'differential_drive_robot'

    # This is the name of our package, at the same time this is the name of the
    # folder that will be used to define the paths
    namePackage = 'mobile_dd_robot'

    # This is a relative path to the xacro file defining the model
    modelFileRelativePath = 'model/robot.xacro'

    # This is a relative path to the Gazebo world file
    worldFileRelativePath = 'model/empty_world.world'

    # This is the absolute path to the model
    pathModelFile = os.path.join(get_package_share_directory(namePackage), modelFileRelativePath)

    pathWorldFile = os.path.join(get_package_share_directory(namePackage),worldFileRelativePath)

    robotDescription = xacro.process_file(pathModelFile).toxml()

    gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('gazebo_ros'),
    'launch', 'gazebo.launch.py'))

    gazeboLaunch = IncludeLaunchDescription(gazebo_rosPackageLaunch, launch_arguments={'world': pathWorldFile}.items())

    spawnModelNode = Node(package='gazebo_ros', executable='spawn_entity.py',
    arguments=['-topic', 'robot_description', '-entity', robotXacroName], output='screen')

    nodeRobotStatePublisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robotDescription,
            'use_sim_time': True}]
    )

    launchDescriptionObject = LaunchDescription()

    launchDescriptionObject.add_action(gazeboLaunch)

    launchDescriptionObject.add_action(spawnModelNode)
    launchDescriptionObject.add_action(nodeRobotStatePublisher)
    
    return launchDescriptionObject

# generate_launch_description()

