from setuptools import setup

long_description = open('README.md', encoding='utf-8').read()

setup(
    name='robodyno',
    version='1.5.1',
    maintainer='robottime',
    maintainer_email='lab@robottime.cn',
    author='song',
    author_email='zhaosongy@126.com',
    description='The Robodyno Robot SDK for Python 3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/robottime/Robodyno-Python-API',
    keywords=['robodyno', 'robot', 'robot module'],
    license='MIT License',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Framework :: Robot Framework',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=[
        'robodyno',
        'robodyno.components',
        'robodyno.components.brands',
        'robodyno.components.can_bus',
        'robodyno.components.webots',
        'robodyno.interfaces',
        'robodyno.tools',
        'robodyno.robots',
        'robodyno.robots.four_dof_palletizing_robot',
        'robodyno.robots.four_dof_scara_robot',
        'robodyno.robots.six_dof_collaborative_robot',
        'robodyno.robots.three_dof_delta_robot',
        'robodyno.robots.three_dof_palletizing_robot',
        'robodyno.robots.utils',
    ],
    package_dir={'robodyno.robots': 'robodyno_robots'},
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.10.0', 
        'colorama>=0.4.5',
        'python-can>=3.2.0, <4.0',
        'importlib-metadata',
    ],
    extras_require={
        ':sys_platform == "win32"': [
            'candle-bus'
        ],
    },
    entry_points={
        'robodyno.components.can_bus': [
            'Motor = robodyno.components.can_bus.motor:Motor',
            'VGripper = robodyno.components.can_bus.vacuum_gripper:VGripper',
            'SliderModule = robodyno.components.can_bus.slider_module:SliderModule',
        ],
        'robodyno.components.webots': [
            'Motor = robodyno.components.webots.motor:Motor',
        ],
        'robodyno.robots': [
            'FourDoFPallet = robodyno.robots.four_dof_palletizing_robot.four_dof_pallet_robot:FourDoFPallet',
            'FourDoFScara = robodyno.robots.four_dof_scara_robot.four_dof_scara_robot:FourDoFScara',
            'SixDoFCollabRobot = robodyno.robots.six_dof_collaborative_robot.six_dof_collab_robot:SixDoFCollabRobot',
            'ThreeDoFDelta = robodyno.robots.three_dof_delta_robot.three_dof_delta_robot:ThreeDoFDelta',
            'ThreeDoFPallet = robodyno.robots.three_dof_palletizing_robot.three_dof_pallet_robot:ThreeDoFPallet',
        ],
        'console_scripts': [
            'robodyno = robodyno:robodyno',
            'robodyno-motor = robodyno:robodyno_motor'
        ],
    }
)
