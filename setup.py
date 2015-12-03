#!/usr/bin/env python

from setuptools import setup

import os
import codecs

__pkgpath__ = os.path.dirname(os.path.abspath(__file__))


def read_text_file(path, mode='r', encoding='utf8'):
    full_path = os.path.join(__pkgpath__, path)
    with codecs.open(full_path, mode, encoding=encoding) as file_:
        return file_.read()

LONG_DESCRIPTION = read_text_file('README.rst')

setup(name='jinja_tornado',
      version='0.1.0',
      description='jinja2 template support for tornado web framework',
      author='thkang2',
      author_email='thkang91@gmail.com',
      url='https://github.com/thkang2/jinja_tornado',
      long_description=LONG_DESCRIPTION,
      packages=['jinja_tornado'],
      install_requires=['tornado', 'Jinja2'],
      license='MIT License',
      zip_safe = False
      )
