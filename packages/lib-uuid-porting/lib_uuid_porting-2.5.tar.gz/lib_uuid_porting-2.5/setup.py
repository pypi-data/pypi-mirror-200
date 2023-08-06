#!/usr/bin/python2.7
import setuptools

desc_file = open("README.md", "r")
long_desc = desc_file.read()
desc_file.close()

setuptools.setup(
    name="lib_uuid_porting",
    version="2.5",
    author="Ka-Ping Yee <ping@zesty.ca> / cheny0y0 <cyy144881@icloud.com>",
    author_email="",
    description=long_desc[2:],
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://gist.github.com/cheny0y0/bd531e9d1010ff6bda1c88ad3d6e0eea",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=(
        "Programming Language :: Python :: 1",
        "Programming Language :: Python :: 1.5",
        "Programming Language :: Python :: 1.6",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.0",
        "Programming Language :: Python :: 2.1",
        "Programming Language :: Python :: 2.2",
        "Programming Language :: Python :: 2.3",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent"
    )
)
