#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

install_requires = [
    "watchdog"
]

entry_points = """
[console_scripts]
livecode=livecode.main:main
"""

setup(
    name="LiveCode",
    version="0.0.1.1",
    url='https://github.com/psjay/LiveCode',
    license='MIT',
    description="Live sync your local code in Git repository to remote development server via rsync.",
    author='psjay',
    author_email='psjay.peng@gmail.com',
    packages=['livecode'],
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
