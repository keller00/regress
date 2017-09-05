#!/usr/bin/env python

from setuptools import setup

setup(
    name='regress',
    version='1.0.0',
    packages=['regress'],
    url='https://github.com/keller00/regress',
    license='MIT',
    author='Mark,Jim',
    author_email='markooo.keller at gmail dot com',
    description='Regression Test Suite',
    entry_points={
        'console_scripts': [
            'regress = regress.regress:main'
        ]
    }
)
