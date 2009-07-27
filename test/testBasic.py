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

if __name__ == '__main__':
    sys.exit(unittest.main())
