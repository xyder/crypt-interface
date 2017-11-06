#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from crypt_interface.__version__ import __version__


def read(fname):
    return open(str(Path(__file__).parent / fname)).read()

classifiers = """
'Development Status :: 2 - Alpha',
'Intended Audience :: Developers',
'License :: OSI Approved :: MIT License',
'Natural Language :: English',
'Programming Language :: Python :: 3.6',
"""

setup(
    name='crypt_interface',
    version=__version__,
    description='Python interface for *crypt variants like VeraCrypt, etc.',
    long_description=read('README.rst'),
    author='Xyder',
    author_email='',
    url='https://github.com/xyder/crypt-interface',
    classifiers=[c.strip() for c in classifiers.splitlines()
                 if c.strip() and not c.startswith('#')],
    include_package_data=True,
    packages=[
        'crypt_interface',
    ],
    install_requires=[
        'pypiwin32==220'
    ]
)
