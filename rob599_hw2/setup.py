from setuptools import find_packages, setup
import os 
from glob import glob

package_name = 'rob599_hw2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ryan',
    maintainer_email='schofier@oregonstate.edu',
    description='Rob 599 HW files',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'speed_limit = rob599_hw2.limit_speed:main', 
            'speed_in = rob599_hw2.speed_in:main',
            'outside_limit = rob599_hw2.outside_limit:main', 
            'service = rob599_hw2.apply_brakes:main',
            'action_server = rob599_hw2.action_server:main', 
            'action_client = rob599_hw2.action_client:main',
            'launch_rocket = rob599_hw2.launch_rocket:main',
        ],
    },
)
