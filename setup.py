#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="systemd_unit",
    version="1.0.2",
    author="Justin Dray",
    author_email="justin@dray.be",
    url="https://github.com/justin8/python-systemd-unit",
    description="This library lets you create and manage systemd unit files",
    packages=find_packages(),
    license="MIT",
    install_requires=[
    ],
    tests_require=["nose",
        "coverage",
        "mock",
    ],
    test_suite="nose.collector",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
    ],
)
