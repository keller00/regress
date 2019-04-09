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
    author='Mark Keller, Jim Wang',
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
    },
    classifiers=[
        'Environment :: Console',
        'Environment :: Other Environment',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ],
)
