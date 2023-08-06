#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

with open("VERSION", "r", encoding="utf-8") as ver:
    version = ver.read()

setuptools.setup(
    name="threefive",
    version=version,
    author="Adrian",
    author_email="spam@iodisco.com",
    description="Pythonic SCTE35",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/threefive",
    install_requires=[
        'new_reader >= 0.1.3',
        "pyaes",
    ],

    scripts=['bin/threefive'],
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.6",
)