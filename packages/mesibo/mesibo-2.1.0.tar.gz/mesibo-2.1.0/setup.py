import setuptools
import os
from setuptools import setup, find_packages, Extension


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

exec(open('src/mesibo/version.py').read())


setuptools.setup(
    name="mesibo", 
    version=__mesibo_version__,
    author="https://mesibo.com",
    author_email="support@mesibo.com",
    description="mesibo is a real-time communication platform with APIs for messaging and calls",
    long_description= read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/mesibo/python",
    project_urls={
        "Bug Tracker": "https://github.com/mesibo/python/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable", 
        "Intended Audience :: Developers", 
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={
        "mesibo": ["clib/*", "clib/*/*", "clib/*/*/*", "clib/*/*/*/*", "clib/*/*/*/*/*"],
    },
    python_requires=">=3.6",
)
