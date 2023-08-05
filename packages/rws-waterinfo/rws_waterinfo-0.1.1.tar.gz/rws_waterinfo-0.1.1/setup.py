#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number,
# edit rws_waterinfo/__init__.py


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.rst") as readme_file:
    readme = readme_file.read()

setup(
    name="rws_waterinfo",
    extras_require={
        "dev": [
            "bandit",
            "black",
            "flake8",
            "flake8-bugbear",
            "flake8-comprehensions",
            "flake8-docstrings",
            "flake8-polyfill",
            "isort",
            "mypy",
            "pre-commit",
            "pylint",
            "pylint[prospector]",
            "pytest",
            "pytest-cov",
            "radon",
            "safety",
            "sh",
        ],
        "doc": [
            "pydata-sphinx-theme",
            "sphinx",
        ],
    },
    tests_require=["pytest", "pytest-cov"],
    test_suite="tests",
    version=find_version("rws_waterinfo", "__init__.py"),
    description="",
    long_description=readme + "\n\n",
    author="RWS Datalab",
    author_email="datalab.codebase@rws.nl",
    url="https://gitlab.com/rwsdatalab/public/codebase/tools/rws-waterinfo",
    packages=["rws_waterinfo"],
    include_package_data=True,
    package_data={"rws_waterinfo": ["py.typed"]},
    license_files=["LICENSE"],
    zip_safe=False,
    keywords="rws_waterinfo",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "numpy",
        "pandas",
        "requests",
        "types-requests",
    ],  # FIXME: add your package's dependencies to this list
    setup_requires=[
        # dependency for `python setup.py test`
        # "pytest-runner",
        # dependencies for `python setup.py build_sphinx`
        # "pydata-sphinx-theme",
        # "sphinx",
        # "sphinxcontrib-pdfembed @ git+https://github.com/SuperKogito/sphinxcontrib-pdfembed",
    ],
)
