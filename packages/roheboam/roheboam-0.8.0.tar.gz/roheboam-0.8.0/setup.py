import pdb
import platform
import sys

from setuptools import find_packages, setup

import roheboam

setup(
    name="roheboam",
    version=roheboam.__version__,
    author="Kevin Lu",
    author_email="kevinyihchyunlu@gmail.com",
    license="GPL3",
    packages=find_packages(exclude=["tests", "tests/*", "examples", "examples/*"]),
    entry_points={
        "console_scripts": [
            "roheboam = roheboam.cli:cli",
        ],
    },
    install_requires=[],
    zip_safe=False,
)
