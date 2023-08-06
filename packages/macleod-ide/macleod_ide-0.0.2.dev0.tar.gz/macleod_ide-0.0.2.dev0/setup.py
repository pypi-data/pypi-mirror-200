# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2023, Reading Club Development
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
macleod_ide setup.
"""
from setuptools import find_packages
from setuptools import setup

from macleod_ide import __version__


setup(
    # See: https://setuptools.readthedocs.io/en/latest/setuptools.html
    name="macleod_ide",
    version=__version__,
    author="Reading Club Development",
    author_email="jesiah.harris4@gmail.com",
    description="An IDE plugin for the macleod parser",
    long_description="A plugin for the macelod parser designed for use in the Spyder IDE",
    long_description_content_type="text/markdown",
    license="GNU General Public License v3",
    url="https://github.com/jesiahharris/macleod_ide",
    python_requires='>= 3.7',
    install_requires=[
        "qtpy",
        "qtawesome",
        "spyder>=5.0.1",
    ],
    packages=find_packages(),
    entry_points={
        "spyder.plugins": [
            "macleod_ide = macleod_ide.spyder.plugin:macleod_ide"
        ],
    },
    classifiers=[
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
    ],
)
