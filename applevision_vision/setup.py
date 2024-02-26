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
            'pub_image = applevision_vision.image_pub:main'
        ],
    },
)
