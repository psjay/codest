#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

install_requires = [
    "watchdog"
]

entry_points = """
[console_scripts]
codest=codest.main:main
"""

setup(
    name="codest",
    version="0.1.2",
    url='https://github.com/psjay/codest',
    license='MIT',
    description="Coding at local like you do it on remote",
    author='psjay',
    author_email='psjay.peng@gmail.com',
    packages=['codest'],
    install_requires=install_requires,
    entry_points=entry_points,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Operating System :: POSIX",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
)
