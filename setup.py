#! /usr/bin/env python
# -*- coding: utf-8 -*-


import pathlib
from setuptools import setup


here = pathlib.Path(__file__).parent


DESCRIPTION = "Like Bootstrap, but qt-er."
LONG_DESCRIPTION = (here / "README.md").read_text()
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Widget Sets",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]


setup(
    name="qtstrap",
    version="0.0.7",
    packages=['qtstrap', 'qtstrap.widgets'],
    install_requires=[
        'PySide2',
        'click',
        'PyInquirer',
        'pyinstaller',
    ],
    entry_points={
        'console_scripts': [
            'qtstrap=qtstrap.__main__:main'
        ]
    },
    include_package_data=True,
    # setup_requires=[],
    # tests_require=[],
    platforms=["any"],
    author="David Kincaid",
    author_email="dlkincaid0@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=CLASSIFIERS,
    keywords=["qtstrap", "qt", "pyqt"],
    url="https://github.com/DaelonSuzuka/qtstrap"
)