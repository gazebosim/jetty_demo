import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'sim_ifaces_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
        # TODO(azeey): Find a nicer way to do this
        (os.path.join('share', package_name, 'models'), glob('models/*.*')),
        (os.path.join('share', package_name, 'models', 'ur10'), glob('models/ur10/*.*')),
        (os.path.join('share', package_name, 'models', 'ur10', 'meshes'), glob('models/ur10/meshes/*.*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Addisu Z. Taddese',
    maintainer_email='addisuzt@intrinsic.ai',
    description='Controls a simulated conveyor belt scenario using simulation_interfaces.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'conveyor_controller = sim_ifaces_demo.conveyor_controller:main'
        ],
    },
)

