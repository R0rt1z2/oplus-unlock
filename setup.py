#!/usr/bin/python3

from setuptools import setup

setup(
    name="oplus-unlock",
    version="1.0",
    description="Tool to patch oplus bootloaders to enable fastboot.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Roger Ortiz",
    url="https://github.com/R0rt1z2/oplus-unlock",
    keywords=["bootloader", "unlock", "oplus", "fastboot"],
    packages=['oplus_unlock', 'oplus_unlock.utils'],
    scripts=['oplus-unlock'],
    license="GPLv3"
)