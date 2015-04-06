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
import unittest

import keyutils

class BasicTest(unittest.TestCase):
    def testSet(self):
        keyDesc = "test:key:01"
        keyVal = "key value with\0 some weird chars in it too"
        keyring = keyutils.KEY_SPEC_THREAD_KEYRING

        # Key not initialized; should get None
        keyId = keyutils.request_key(keyDesc, keyring)
        self.failUnlessEqual(keyId, None)

        self.failUnlessRaises(keyutils.Error, keyutils.read_key, 12345L)
        try:
            keyutils.read_key(12345L)
        except keyutils.Error, e:
            self.failUnlessEqual(e.args, (126, 'Required key not available'))

        keyutils.add_key(keyDesc, keyVal, keyring)
        keyId = keyutils.request_key(keyDesc, keyring)

        data = keyutils.read_key(keyId)
        self.failUnlessEqual(data, keyVal)

    def testSession(self):
        desc = "test:key:02"
        val = "asdfasdfasdf"
        session = keyutils.join_session_keyring()
        keyId = keyutils.add_key(desc, val, session)
        self.assertEqual(keyutils.search(keyutils.KEY_SPEC_SESSION_KEYRING,
            desc), keyId)
        keyutils.join_session_keyring()
        self.assertEqual(keyutils.search(keyutils.KEY_SPEC_SESSION_KEYRING,
            desc), None)

    def testRevoke(self):
        desc = "dummy"
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
        desc = "key1"
        child = keyutils.add_key("ring1", None, keyutils.KEY_SPEC_PROCESS_KEYRING, "keyring")
        parent = keyutils.add_key("ring2", None, keyutils.KEY_SPEC_PROCESS_KEYRING, "keyring")
        keyId = keyutils.add_key(desc, "dummy", child)
        self.assertEqual(keyutils.search(child, desc), keyId)
        self.assertEqual(keyutils.search(parent, desc), None)
        keyutils.link(child, parent)
        self.assertEqual(keyutils.search(parent, desc), keyId)


if __name__ == '__main__':
    sys.exit(unittest.main())
