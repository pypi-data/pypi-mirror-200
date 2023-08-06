"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

setup(
    name="dot_to_object",
    author="Enes Doğan",
    author_email="enesdogan26@gmail.com",
    url="https://github.com/enesdogan00/dot_to_object",
    description="A module to return python objects from dot notation strings.",
    version="0.0.2",
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=[
        "setuptools>=45.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)