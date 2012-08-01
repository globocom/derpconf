#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from setuptools import setup
from derpconf.version import __version__

def run_setup(extension_modules = []):
  setup(
      name = 'derpconf',
      version = __version__,
      description = "derpconf abstracts loading configuration files for your app",
      long_description = """
derpconf abstracts loading configuration files for your app.
""",
      keywords = 'configuration',
      author = 'globo.com',
      author_email = 'timehome@corp.globo.com',
      url = 'https://github.com/globocom/derpconf',
      license = 'MIT',
      classifiers = ['Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Natural Language :: English',
                     'Operating System :: MacOS',
                     'Operating System :: POSIX :: Linux',
                     'Programming Language :: Python :: 2.6',
      ],
      packages = ['derpconf'],
      package_dir = {"derpconf": "derpconf"},
      include_package_data = False
  )

run_setup()
