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


import _keyutils
for k, v in _keyutils.__dict__.items():
    if k.startswith('E') or k.startswith('KEY_SPEC_'):
        globals()[k] = v
del k, v

Error = _keyutils.error

def add_key(key, value, keyring, keyType = "user"):
    return _keyutils.add_key(keyType, key, value, keyring)

def request_key(key, keyring, keyType = "user"):
    return _keyutils.request_key(keyType, key, keyring)

def read_key(keyId):
    return _keyutils.read_key(keyId)
