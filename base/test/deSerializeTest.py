import unittest
import logging
import sys

sys.path.append('../')

from base.remoteMeDataReader import RemoteMeDataReader

logger = logging.getLogger('remoteMe.RemoteMeData')

class TestDeSerialize(unittest.TestCase):

    def test_upper(self):
        data = '\x00\x01\x01\x02\x03\x05\x08'
        rmData = RemoteMeDataReader(data)
        self.assertEqual( 0,rmData.readInt8())
        self.assertEqual( 1,rmData.readInt8())
        self.assertEqual( 1,rmData.readInt8())
        self.assertEqual( 2,rmData.readInt8())
        self.assertEqual( 3,rmData.readInt8())
        self.assertEqual( 5,rmData.readInt8())
        self.assertEqual( 8,rmData.readInt8())

    def testStringAndUint(self):
        data = '\x6d\x61\x63\x69\x65\x6b\x74\x65\x73\x74\x00\x6d\x61\x00\x23'
        rmData = RemoteMeDataReader(data)
        self.assertEqual( "maciektest",rmData.readString())
        self.assertEqual( "ma",rmData.readString())
        self.assertEqual(0x23,rmData.readInt8() )





if __name__ == '__main__':
    unittest.main()