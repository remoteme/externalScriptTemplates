import unittest
import logging
import sys

from base.remoteMeDataWriter import RemoteMeDataWriter

sys.path.append('../')

from base.remoteMeDataReader import RemoteMeDataReader

logger = logging.getLogger('remoteMe.RemoteMeData')

class TestSerialize(unittest.TestCase):

    def test_readString(self):
        rmData = RemoteMeDataWriter()
        rmData.writeString("maciek")
        rmData.writeInt8(0x0F)
        rmData.writeInt8(0x10)
        rmData.writeInt8(-5)


        print(rmData.getBytesAsHexString())


        reader = RemoteMeDataReader(rmData.getBytes())

        self.assertEqual('maciek', reader.readString())
        self.assertEqual(0x0F10, reader.readInt16())
        self.assertEqual(-5, reader.readInt8())


    def test_readString(self):
        rmData = RemoteMeDataWriter()
        rmData.writeString("漢語拼音")
        rmData.writeString("maciekśćół")
        rmData.writeString("देवनागरी")


        print(rmData.getBytesAsHexString())


        reader = RemoteMeDataReader(rmData.getBytes())

        self.assertEqual('漢語拼音', reader.readString())
        self.assertEqual('maciekśćół', reader.readString())
        self.assertEqual('देवनागरी', reader.readString())

    def test_readString(self):
        writer = RemoteMeDataWriter()
        writer.writeString("maciekśćół")
        writer.writeInt8(123)
        writer.writeInt8(-53)
        writer.writeUInt8(240)
        writer.writeUInt16(65531)
        writer.writeInt16(-15531)


        print(writer.getBytesAsHexString())

        reader = RemoteMeDataReader(writer.getBytes())

        self.assertEqual('maciekśćół',reader.readString())
        self.assertEqual(123,reader.readInt8())
        self.assertEqual(-53,reader.readInt8())
        self.assertEqual(240,reader.readUInt8())
        self.assertEqual(65531, reader.readUInt16())
        self.assertEqual(-15531,reader.readInt16())



if __name__ == '__main__':
    unittest.main()