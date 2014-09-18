from setuptools import setup, find_packages # Always prefer setuptools over distutils
setup(
name='python-depot',
# Versions should comply with PEP440. For a discussion on single-sourcing
# the version across setup.py and the project code, see
# http://packaging.python.org/en/latest/tutorial.html#version
version='0.99',
description='Shared variables for python processes',
long_description="Easy way to share a python data structure between modules in python using multiprocessing.Manager",
# The project's main homepage.
url='https://github.com/atmb4u/depot',
# Author details
author='Anoop Thomas Mathew',
author_email='atmb4u@gmail.com',
# Choose your license
license='3-clause BSD License',
scripts=['depot', 'daemon.py'],
# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers=[
'Development Status :: 4 - Beta',
'Intended Audience :: Developers',
'Topic :: Software Development :: Build Tools',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 2',
'Programming Language :: Python :: 2.6',
'Programming Language :: Python :: 2.7',
'License :: OSI Approved :: BSD License',
'Environment :: Console',
'Topic :: Software Development :: Libraries :: Python Modules',
],
# What does your project relate to?
keywords='depot persistent dictionary development shared variables',
install_requires=['python-daemon'],
)
