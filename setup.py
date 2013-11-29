#!/usr/bin/env python

from distutils.core import setup

setup(
    name='pyr',
    version='0.1',
    description='A nicer REPL for Python.',
    author='Zain Memon',
    author_email='zain@inzain.net',
    url='https://github.com/zain/pyr',
    packages=['pyr'],
    install_requires=['pygments'],
    entry_points={
        'console_scripts': [
            'pyr = pyr.shell:main',
        ],
    },
    scripts=['bin/pyr'],
)
