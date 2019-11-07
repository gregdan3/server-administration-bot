#!/usr/bin/env python3

import io
import os
from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))

REQUIRED = ["python-telegram-bot", "pyyaml"]

TEST_REQUIREMENTS = ["pytest"]

EXTRAS = {}

# Load the package's __version__.py module as a dictionary.
about = {}
with open(
    os.path.join(here, "sysadmin_telebot", "__version__.py"), "r", encoding="utf-8"
) as f:
    exec(f.read(), about)


# readme has to be in Manifest
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = about["__description__"]


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=["__author__"],
    author_email=["__author_email__"],
    python_requires=">=3.6.6",
    url=about["__url__"],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    tests_require=TEST_REQUIREMENTS,
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
