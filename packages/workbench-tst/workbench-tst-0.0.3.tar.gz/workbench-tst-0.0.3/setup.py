#!/usr/bin/env python3

import os
from io import open

from setuptools import find_packages, setup


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


setup(
    name="workbench-tst",
    version=__import__("workbench_tst").__version__,
    description="Command-line interface to Workbench's timestamps",
    # long_description=read("README.rst"),
    author="Matthias Kestenholz",
    author_email="mk@feinheit.ch",
    url="https://github.com/matthiask/workbench-tst/",
    license="BSD License",
    platforms=["OS Independent"],
    packages=find_packages(exclude=["tests", "testapp"]),
    include_package_data=True,
    entry_points={"console_scripts": ["tst=workbench_tst.command_line:main"]},
    zip_safe=False,
)
