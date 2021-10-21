import sys
from setuptools import setup, find_packages


with open("README.md") as desc:
    long_description = desc.read()

setup(
    name="async-data-flow",
    version="0.0.2",
    description="Asynchronous data flow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Tomasz Król',
    author_email='tomasz.kingu.krol@gmail.com',
    maintainer='Tomasz Król',
    maintainer_email='tomasz.kingu.krol@gmail.com',
    url='https://github.com/tomaszkingukrol/async-data-flow',
    project_urls={
        "Bug Tracker": "https://github.com/tomaszkingukrol/async-data-flow/issues",
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)