#!/usr/bin/env python

from setuptools import setup

setup(
    name='pyr',
    version='0.3',
    description='A nicer REPL for Python.',
    author='Zain Memon',
    author_email='zain@inzain.net',
    url='https://github.com/zain/pyr',
    packages=['pyr'],
    install_requires=['pygments'],
    scripts=['bin/pyr'],
)
