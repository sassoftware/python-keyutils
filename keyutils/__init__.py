#!/usr/bin/python
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

from __future__ import absolute_import


from . import _keyutils
for k, v in _keyutils.constants.__dict__.items():
    globals()[k] = v
del k, v

from errno import EINVAL, ENOMEM, EDQUOT, EINTR, EACCES

Error = _keyutils.error

def add_key(key, value, keyring, keyType=b"user"):
    return _keyutils.add_key(keyType, key, value, keyring)


def request_key(key, keyring, keyType=b"user"):
    try:
        return _keyutils.request_key(keyType, key, None, keyring)
    except Error as err:
        if err.args[0] == _keyutils.constants.ENOKEY:
            return None
        raise


def search(keyring, description, destination=0, keyType=b"user"):
    try:
        return _keyutils.search(keyring, keyType, description, destination)
    except Error as err:
        if err.args[0] == _keyutils.constants.ENOKEY:
            return None
        raise


def read_key(keyId):
    return _keyutils.read_key(keyId)


def join_session_keyring(name=None):
    return _keyutils.join_session_keyring(name)


def link(key, keyring):
    return _keyutils.link(key, keyring)


def unlink(key, keyring):
    return _keyutils.unlink(key, keyring)


def revoke(key):
    return _keyutils.revoke(key)


def set_timeout(key, timeout):
    """Set timeout in seconds."""
    return _keyutils.set_timeout(key, timeout)
