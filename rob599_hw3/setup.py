from setuptools import find_packages, setup
import os 
from glob import glob

package_name = 'rob599_hw3'

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
    description='Files for Rob599 HW 3',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'places = rob599_hw3.places:main',
            'services = rob599_hw3.services:main', 
            'go_to_action_client = rob599_hw3.go_to_client:main',
            'patrol_action_client = rob599_hw3.patrol_client:main',
            'knock_knock_client = rob599_hw3.knock_knock_client:main', 
            'knock_knock_server = rob599_hw3.knock_knock_server:main'
        ],
    },
)
