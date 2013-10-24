#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup, find_packages

setup(
    name             = 'Django-key-auth',
    version          = '1.0.0',
    author           = "Diogo Laginha",
    url              = 'https://github.com/laginha/django-key-auth',
    description      = "Key based authentication for Django",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = ['rstr'],
    extras_require   = {},
    zip_safe         = False,
)
