import os
from setuptools import setup, find_packages

setup(
    name="durin",
    version=os.getenv("VERSION"),
    packages=find_packages(),
)
