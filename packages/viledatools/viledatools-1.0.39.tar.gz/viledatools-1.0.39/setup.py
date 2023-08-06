# coding=utf-8
"""
viledatools

python setup.py sdist bdist_wheel
twine upload --config-file E:/twine-config-pypi.pypirc dist/*1.0.39*
"""

from setuptools import setup

setup(name='viledatools',
      version='1.0.39',
      packages=['viledatools'],
      url='https://www.vileda-professional.com/',
      license='Creative Commons Attribution 4.0 International',
      author='FHCS GmbH',
      author_email='support@fhcs.zendesk.com',
      description='Classes and functions to use for development of intregration software',
      install_requires=['aiohttp>=3.8.3', 'openpyxl>=3.0.10'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Other Environment',
                   'License :: Other/Proprietary License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.8',
                   'Topic :: Utilities'],
      zip_safe=False,
      python_requires='>=3.8'
      )
