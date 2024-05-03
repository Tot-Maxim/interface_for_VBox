#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup, find_packages

setup(name='python-pytuntap',
      py_modules = ["tuntap"],
      author='totmaxim',
      author_email='boom.rezonans@yanex.ru',
      maintainer='maxim',
      url='https://github.com/Tot-Maxim/interface_for_VBox',
      description='Linux/Windows TUN/TAP wrapper for Python',
      long_description=open('README.rst').read(),
      version='1.0.5',
      #install_requires=[        'pywin32',        ],
      python_requires='>=3',
      platforms=["Linux","Windows"],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Networking'])
