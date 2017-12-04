#!/usr/bin/env python

from setuptools import setup
from regress import VERSION

try:
    import pypandoc
    LONG_DESC = pypandoc.convert("README.md", "rst")
except (IOError, ImportError, RuntimeError):
    LONG_DESC = open('README.md').read()

setup(
    name='regress',
    version=VERSION,
    packages=['regress'],
    url='https://github.com/keller00/regress',
    license='MIT',
    author='Mark,Jim',
    author_email='markooo.keller at gmail dot com',
    description='Regression Test Suite',
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    long_description=LONG_DESC,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'regress = regress:main'
        ]
    }
)
