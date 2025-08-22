from setuptools import setup, find_packages
import os

setup(
    name="durin",
    version=os.getenv("VERSION"),
    packages=find_packages(),
)
