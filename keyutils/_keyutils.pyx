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

from libc cimport stdlib

cdef extern from "Python.h":
    object PyErr_SetFromErrno(exc)
    object PyBytes_FromStringAndSize(char *str, Py_ssize_t size)

cdef extern from "keyutils.h" nogil:
    int c_KEY_SPEC_THREAD_KEYRING "KEY_SPEC_THREAD_KEYRING"
    int c_KEY_SPEC_PROCESS_KEYRING "KEY_SPEC_PROCESS_KEYRING"
    int c_KEY_SPEC_SESSION_KEYRING "KEY_SPEC_SESSION_KEYRING"
    int c_KEY_SPEC_USER_KEYRING "KEY_SPEC_USER_KEYRING"
    int c_KEY_SPEC_USER_SESSION_KEYRING "KEY_SPEC_USER_SESSION_KEYRING"
    int c_ENOKEY "ENOKEY"
    int c_EKEYEXPIRED "EKEYEXPIRED"
    int c_EKEYREVOKED "EKEYREVOKED"
    int c_EKEYREJECTED "EKEYREJECTED"
    int c_add_key "add_key"(char *key_type, char *description, void *payload,
            int plen, int keyring)
    int c_request_key "request_key"(char *key_type, char *description,
            char *callout_info, int keyring)
    int c_search "keyctl_search"(int keyring, char *key_type,
            char *description, int destination)
    int c_read_alloc "keyctl_read_alloc"(int key, void **bufptr)
    int c_join_session_keyring "keyctl_join_session_keyring"(char *name)
    int c_session_to_parent "keyctl_session_to_parent"()
    int c_link "keyctl_link"(int key, int keyring)
    int c_unlink "keyctl_unlink"(int key, int keyring)
    int c_revoke "keyctl_revoke"(int key)
    int c_set_timeout "keyctl_set_timeout" (int key, int timeout)
    int c_clear "keyctl_clear" (int keyring)
    int c_describe_alloc "keyctl_describe_alloc" (int key, char **bufptr)


class error(Exception):
    pass


class constants:
    KEY_SPEC_THREAD_KEYRING = c_KEY_SPEC_THREAD_KEYRING
    KEY_SPEC_PROCESS_KEYRING = c_KEY_SPEC_PROCESS_KEYRING
    KEY_SPEC_SESSION_KEYRING = c_KEY_SPEC_SESSION_KEYRING
    KEY_SPEC_USER_KEYRING = c_KEY_SPEC_USER_KEYRING
    KEY_SPEC_USER_SESSION_KEYRING = c_KEY_SPEC_USER_SESSION_KEYRING
    ENOKEY = c_ENOKEY
    EKEYEXPIRED = c_EKEYEXPIRED
    EKEYREVOKED = c_EKEYREVOKED
    EKEYREJECTED = c_EKEYREJECTED


def add_key(bytes key_type, bytes description, bytes payload, int keyring):
    cdef int rc
    cdef char *key_type_p = key_type
    cdef char *desc_p = description
    cdef int payload_len
    cdef char *payload_p
    if payload is None:
        payload_p = NULL
        payload_len = 0
    else:
        payload_p = payload
        payload_len = len(payload)
    with nogil:
        rc = c_add_key(key_type_p, desc_p, payload_p, payload_len, keyring)
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return rc


def request_key(bytes key_type, bytes description, bytes callout_info, int keyring):
    cdef char *key_type_p = key_type
    cdef char *desc_p = description
    cdef char *callout_p
    cdef int rc
    if callout_info is None:
        callout_p = NULL
    else:
        callout_p = callout_info
    with nogil:
        rc = c_request_key(key_type_p, desc_p, callout_p, keyring)
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return rc


def search(int keyring, bytes key_type, bytes description, int destination):
    cdef char *key_type_p = key_type
    cdef char *desc_p = description
    cdef int rc
    with nogil:
        rc = c_search(keyring, key_type_p, desc_p, destination)
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return rc


def read_key(int key):
    cdef int size
    cdef void *ptr
    cdef bytes obj
    with nogil:
        size = c_read_alloc(key, &ptr)
    if size < 0:
        PyErr_SetFromErrno(error)
    else:
        obj = PyBytes_FromStringAndSize(<char*>ptr, size)
        stdlib.free(ptr)
        return obj


def describe_key(int key):
    cdef int size
    cdef char *ptr
    cdef bytes obj
    with nogil:
        size = c_describe_alloc(key, &ptr)
    if size < 0:
        PyErr_SetFromErrno(error)
    else:
        obj = PyBytes_FromStringAndSize(<char*>ptr, size)
        stdlib.free(ptr)
        return obj


def join_session_keyring(name):
    cdef char *name_p
    cdef int rc
    if name is None:
        name_p = NULL
    else:
        name_p = name
    with nogil:
        rc = c_join_session_keyring(name_p)
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return rc


def session_to_parent():
    cdef int rc
    with nogil:
        rc = c_session_to_parent()
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return None


def link(int key, int keyring):
    cdef int rc
    with nogil:
        rc = c_link(key, keyring)
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return None


def unlink(int key, int keyring):
    cdef int rc
    with nogil:
        rc = c_unlink(key, keyring)
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return None


def revoke(int key):
    cdef int rc
    with nogil:
        rc = c_revoke(key)
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return None


def set_timeout(int key, int timeout):
    cdef int rc
    with nogil:
        rc = c_set_timeout(key, timeout)
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return None


def clear(int keyring):
    cdef int rc
    with nogil:
        rc = c_clear(keyring)
    if rc < 0:
        PyErr_SetFromErrno(error)
    else:
        return None
