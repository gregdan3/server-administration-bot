#!/usr/bin/env python3

import io
import os
from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as f:
    REQUIRED = [line.strip() for line in f.readlines()]

EXTRAS = {}

TEST_REQUIREMENTS = ["pytest>=2.8.0"]

# Load the package's __version__.py module as a dictionary.
about = {}
with open(
    os.path.join(here, "sysadmin_telebot", "__version__.py"), "r", encoding="utf-8"
) as f:
    exec(f.read(), about)


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
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
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    tests_require=TEST_REQUIREMENTS,
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
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
