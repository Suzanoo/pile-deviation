
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
from setuptools import find_packages
from setuptools import setup

setup(
    name='tools',
    version='0.1',
    license='',
    description='make package from tools directory',
    url='',
    author='Suzanoo',
    author_email='highwaynumber12@gmail.com',
    packages=find_packages(exclude=['data']),
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
        'dash',
        'dash_bootstrap_components',
        'setuptools'
    ],

    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    

    )
# install package:
# % python setup.py install