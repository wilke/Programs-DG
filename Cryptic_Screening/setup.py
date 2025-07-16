#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="cryptic-screening",
    version="1.0.0",
    description="Files used to screen SRA samples for cryptic signals",
    author="Cryptic Screening Team",
    python_requires=">=3.6",
    install_requires=[
        "pysam",
    ],
    scripts=[
        "NTSeqScreenMP.py",
        "PMScreenMP.py", 
        "WinnowScreens.py",
    ],
    data_files=[
        (".", ["LinkedPMs.txt", "SinglePMs.txt"]),
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)