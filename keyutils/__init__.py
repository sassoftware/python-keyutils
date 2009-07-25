#!/usr/bin/python
#
# Copyright (c) 2009 rPath, Inc.
#
# This program is distributed under the terms of the Common Public License,
# version 1.0. A copy of this license should have been distributed with this
# source file in a file called LICENSE. If it is not present, the license
# is always available at http://www.rpath.com/permanent/licenses/CPL-1.0.
#
# This program is distributed in the hope that it will be useful, but
# without any warranty; without even the implied warranty of merchantability
# or fitness for a particular purpose. See the Common Public License for
# full details.
#

import _keyutils
for k, v in _keyutils.__dict__.items():
    if k.startswith('E'):
        globals()[k] = v
del k, v

def add_key(key, value, keyring, keyType = "user"):
    return _keyutils.add_key(keyType, key, value, keyring)

def request_key(key, keyring, keyType = "user"):
    return _keyutils.request_key(keyType, key, keyring)

def read_key(keyId):
    return _keyutils.read_key(keyId)
