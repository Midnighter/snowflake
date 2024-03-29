#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import io
import re
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup
from glob import glob


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


if __name__ == "__main__":
    setup(
        name="snowflake",
        version="0.1.0",
        license="BSD 3-Clause",
        description="Snowflake Design Pattern",
        long_description="%s\n%s" % (read("README.rst"), re.sub(":obj:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst"))),
        author="Moritz Emanuel Beber",
        author_email="moritz.beber@gmail.com",
        url="https://github.com/Midnighter/snowflake",
        packages=find_packages("src"),
        package_dir={"": "src"},
        py_modules=[splitext(basename(i))[0] for i in glob("src/*.py")],
        include_package_data=False,
        zip_safe=False,
        classifiers=[
            # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Natural Language :: English",
            "Operating System :: Unix",
            "Operating System :: POSIX",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development",
        ],
        keywords=[
            # eg: "keyword1", "keyword2", "keyword3",
        ],
        install_requires=[
            # eg: "aspectlib==1.1.1", "six>=1.7",
        ],
        extras_require={
            # eg: 'rst': ["docutils>=0.11"],
        },
    )

