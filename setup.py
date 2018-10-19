# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='qctools',
    version='0.1.0',
    description='Tools for QuantConnect.com',
    long_description=readme,
    author='Numeris LLC',
    author_email='admin@numeris.tech',
    url='numeris.tech',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
