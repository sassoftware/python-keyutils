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


import sys
import time
import unittest

import keyutils

class BasicTest(unittest.TestCase):
    def testSet(self):
        keyDesc = b"test:key:01"
        keyVal = b"key value with\0 some weird chars in it too"
        keyring = keyutils.KEY_SPEC_THREAD_KEYRING

        # Key not initialized; should get None
        keyId = keyutils.request_key(keyDesc, keyring)
        self.assertEqual(keyId, None)

        self.assertRaises(keyutils.Error, keyutils.read_key, 12345)
        try:
            keyutils.read_key(12345)
        except keyutils.Error as e:
            self.assertEqual(e.args, (126, 'Required key not available'))

        keyutils.add_key(keyDesc, keyVal, keyring)
        keyId = keyutils.request_key(keyDesc, keyring)

        data = keyutils.read_key(keyId)
        self.assertEqual(data, keyVal)

    def testSession(self):
        desc = b"test:key:02"
        val = b"asdfasdfasdf"
        session = keyutils.join_session_keyring()
        keyId = keyutils.add_key(desc, val, session)
        self.assertEqual(keyutils.search(keyutils.KEY_SPEC_SESSION_KEYRING,
            desc), keyId)
        keyutils.join_session_keyring()
        self.assertEqual(keyutils.search(keyutils.KEY_SPEC_SESSION_KEYRING,
            desc), None)

    def testRevoke(self):
        desc = b"dummy"
        session = keyutils.join_session_keyring()
        self.assertEqual(keyutils.search(keyutils.KEY_SPEC_SESSION_KEYRING,
            desc), None)
        keyutils.revoke(session)
        try:
            keyutils.search(keyutils.KEY_SPEC_SESSION_KEYRING, desc)
        except keyutils.Error as err:
            self.assertEqual(err.args[0], keyutils.EKEYREVOKED)
        else:
            self.fail("Expected keyutils.Error")
        keyutils.join_session_keyring()

    def testLink(self):
        desc = b"key1"
        child = keyutils.add_key(b"ring1", None, keyutils.KEY_SPEC_PROCESS_KEYRING, b"keyring")
        parent = keyutils.add_key(b"ring2", None, keyutils.KEY_SPEC_PROCESS_KEYRING, b"keyring")
        keyId = keyutils.add_key(desc, b"dummy", child)
        self.assertEqual(keyutils.search(child, desc), keyId)
        self.assertEqual(keyutils.search(parent, desc), None)
        keyutils.link(child, parent)
        self.assertEqual(keyutils.search(parent, desc), keyId)

    def testTimeout(self):
        desc = b"dummyKey"
        value = b"dummyValue"
        keyring = keyutils.KEY_SPEC_THREAD_KEYRING

        # create key with 1 second timeout:
        keyId = keyutils.add_key(desc, value, keyring)
        keyutils.set_timeout(keyId, 1)

        self.assertEqual(keyutils.request_key(desc, keyring), keyId)
        time.sleep(1.5)
        self.assertEqual(keyutils.request_key(desc, keyring), None)



if __name__ == '__main__':
    sys.exit(unittest.main())
