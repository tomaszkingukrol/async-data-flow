import sys
from setuptools import setup


if sys.version_info < (3, 6, 0):
    raise RuntimeError("async-data-flow requires Python 3.6.0+")

with open("README.md") as desc:
    long_description = desc.read()

setup(
    name="async-data-flow",
    version="0.0.1",
    description="Asynchronous data flow",
    long_description=long_description,
    author='Tomasz Król',
    author_email='tomasz.kingu.krol@gmail.com',
    maintainer='Tomasz Król',
    maintainer_email='tomasz.kingu.krol@gmail.com',
    url='https://github.com/tomaszkingukrol/async-data-flow',
    download_url='https://github.com/tomaszkingukrol/async-data-flow/archive/refs/tags/0.0.1.tar.gz',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=['asyncdataflow']
)