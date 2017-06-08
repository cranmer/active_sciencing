
import os
from setuptools import setup, find_packages

setup(
  name = 'fast-weinberg',
  version = '0.0.1',
  description = 'fast approximation of weinberg madgraph workflow',
  url = '',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages = find_packages(),
  include_package_data = True,
  install_requires = [],
  entry_points = {
      'console_scripts': [
          'weinberg-fast=fastweinberg.main:main',
      ],
  }
)
