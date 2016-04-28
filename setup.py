#!/usr/bin/env python

from setuptools import setup

import os
import codecs

__pkgpath__ = os.path.dirname(os.path.abspath(__file__))


def read_text_file(path, mode='r', encoding='utf8'):
    full_path = os.path.join(__pkgpath__, path)
    with codecs.open(full_path, mode, encoding=encoding) as file_:
        return file_.read()

LONG_DESCRIPTION = u'\n\n'.join((
    read_text_file('README.rst'),
    read_text_file('HISTORY.rst'),
))

setup(name='jinja_tornado',
      version='0.1.1',
      description='jinja2 template support for tornado web framework',
      author='thkang2, westurner',
      author_email='wes@wrd.nu',
      url='https://github.com/westurner/jinja_tornado',
      long_description=LONG_DESCRIPTION,
      packages=['jinja_tornado'],
      install_requires=['tornado', 'Jinja2'],
      license='MIT License',
      zip_safe = False,
      classifers=[
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet',
        'Topic :: Utilities',
    ],
      )
