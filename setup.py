import sys
from setuptools import setup

setup(
    name='asyncdataflow',
    version='0.0.1',
    packages=['asyncdataflow']
)

if sys.version_info < (3, 6, 0):
    raise RuntimeError("async-data-flow requires Python 3.6.0+")

with open("README.md") as desc:
    long_description = desc.read()

setup(
    name="async-data-flow",
    version="0.0.1",
    description="Asynchronous data flow",
    long_description=long_description,
    url="https://github.com/tomaszkingukrol/async-data-flow",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=['asyncdataflow']
)