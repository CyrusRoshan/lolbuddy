#!/usr/bin/env python3

from setuptools import setup, find_packages

version = '0.2.0'

setup(
    name='lolbuddy',
    version=version,
    description='a cli tool to update league of legends itemsets and ability order from champion.gg',
    author='Cyrus Roshan',
    author_email='hello@cyrusroshan.com',
    license='MIT',
    keywords=['lol', 'league', 'league of legends', 'item', 'ability'],
    url='https://github.com/CyrusRoshan/lolbuddy',
    packages=find_packages(),
    package_data={},
    install_requires=[
        'requests-futures >= 0.9.5',
    ],
    entry_points={
        'console_scripts': [
            'lolbuddy=lolbuddy:main',
        ],
    },
)
