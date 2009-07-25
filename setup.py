#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    name='python-keyutils',
    version='0.1',
    description='keyutils bindings for Python',
    author='Mihai Ibanescu',
    author_email='misa@rpath.com',
    url='http://www.rpath.com',
    license='CPL',
    packages=['keyutils'],
    ext_modules=[
        Extension(
            'keyutils._keyutils', ['keyutils/_keyutils.c'], libraries=['keyutils'],
        )
    ],
)
