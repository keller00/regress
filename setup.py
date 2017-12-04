#!/usr/bin/env python

from setuptools import setup, Command
from regress import VERSION

try:
    import pypandoc
    LONG_DESC = pypandoc.convert("README.md", "rst")
except (IOError, ImportError, RuntimeError):
    LONG_DESC = open('README.md').read()


class PandocCommand(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        from pypandoc.pandoc_download import download_pandoc
        # see the documentation how to customize the installation path
        # but be aware that you then need to include it in the `PATH`
        download_pandoc()


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
    },
    cmdclass={'get_pandoc': PandocCommand},
)
