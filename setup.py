import os
from setuptools import setup, find_packages


setup(name='stocks',
      setup_requires=[
          'setuptools_scm',
      ],
      tests_require=[
          'pytest==3.8.0',
          'mock==2.0.0',
      ],
      version='0.1',
      url='',
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['stocks'],
      zip_safe=False)
