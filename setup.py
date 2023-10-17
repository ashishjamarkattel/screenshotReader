import os
from setuptools import setup, find_namespace_packages


with open("requirements.txt", "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]


setup(
    name="screenshotreader",
    description= "Easy assible for the screenshot",
    version=0.0,
    packages=find_namespace_packages(),
    install_requires= required_packages
)