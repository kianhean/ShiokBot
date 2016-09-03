# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ShiokBot',
    version='0.0.1',
    description='ShiokBot Code',
    long_description=readme,
    author='xxxx',
    author_email='xxxxx',
    url='xxxx',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
