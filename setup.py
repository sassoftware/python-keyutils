#!/usr/bin/env python
#
# Copyright (c) SAS Institute Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from distutils.core import setup, Extension

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='keyutils',
    version='0.3',
    description='keyutils bindings for Python',
    long_description=long_description,
    author='Mihai Ibanescu',
    author_email='mihai.ibanescu@sas.com',
    url='https://github.com/sassoftware/python-keyutils',
    license='Apache 2.0',
    packages=['keyutils'],
    classifiers=[
        "Topic :: Security",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        ],
    platforms=[
        "Linux",
        ],
    ext_modules=[
        Extension(
            'keyutils._keyutils', ['keyutils/_keyutils.c'], libraries=['keyutils'],
        )
    ],
)
