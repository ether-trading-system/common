from setuptools import setup, find_packages
from pathlib import Path

import importlib.metadata
import toml


def read_version():
    pyproject = toml.load("pyproject.toml")
    return pyproject["tool"]["poetry"]["version"]


def read_requirements():
    pyproject = toml.load("pyproject.toml")
    return pyproject["tool"]["poetry"]["dependencies"]


setup(
    name='quant-common',
    version=read_version(),
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    author='dalcon10028',
    author_email='dalcon10280@gmail.com',
    install_requires=read_requirements(),
)
