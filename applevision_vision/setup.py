from setuptools import find_packages, setup

package_name = 'applevision_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ryan',
    maintainer_email='schofier@oregonstate.edu',
    description='The applevision_rospkg package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'applevision_vision = applevision_vision.applevision_vision:main', 
            'pub_image = applevision_vision.image_pub:main', 
            'find_center = applevision_vision.find_center:main',
            'move = applevision_vision.move_arm:main',
            'move_service = applevision_vision.move_arm_with_service_calls:main',
            'speed_service = applevision_vision.speed_service:main',
            'distance_service = applevision_vision.distance_service:main',
            'tof_fake = applevision_vision.tof_pub_fake:main'
        ],
    },
)
