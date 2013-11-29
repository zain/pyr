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
    requires=['pygments'],
    scripts=['bin/pyr'],
)
