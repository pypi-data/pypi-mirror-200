# This file is placed in the Public Domain.


"object programming quest"


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="opq",
    version="13",
    author="Bart Thate",
    author_email="operbot100@gmail.com",
    url="http://github.com/operbot/opq",
    zip_safe=True,
    description="object programming quest",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["opq", "opq.modules"],
    scripts=["bin/opq"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
