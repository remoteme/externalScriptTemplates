import unittest
import logging
import sys
import time

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


    def test_writeData(self):


        writer2 = RemoteMeDataWriter()
        writer2.writeInt8(1)
        writer2.writeInt8(2)
        writer2.writeInt8(3)
        writer2.writeInt8(5)
        writer2.writeInt8(8)
        writer2.writeInt8(13)

        writer = RemoteMeDataWriter()

        writer.writeData([1,2,3,4])
        writer.writeData(writer2.getBytes())

        reader = RemoteMeDataReader(writer.getBytes())
        self.assertEqual([1,2,3,4,1,2,3,5,8,13], reader.readData(10))

        writer.writeInt8(100)
        reader = RemoteMeDataReader(writer.getBytes()) #reset
        writer.writeData( reader.readData(10))

        reader= RemoteMeDataReader(writer.getBytes())
        self.assertEqual([1, 2, 3, 4, 1, 2, 3, 5, 8, 13,100,1, 2, 3, 4, 1, 2, 3, 5, 8, 13], reader.readData(21))

    def test_writeData(self):
        writer = RemoteMeDataWriter()
        writer.writeInt32(-2147483648)
        writer.writeUInt32(2147483647+1000)

        writer.writeInt16(-32767)
        writer.writeUInt16(32767 + 1000)

        writer.writeInt8(-128)
        writer.writeUInt8(255)

        reader = RemoteMeDataReader(writer.getBytes())
        self.assertEqual(-2147483648, reader.readInt32())
        self.assertEqual(2147483647+1000, reader.readUInt32())

        self.assertEqual(-32767, reader.readInt16())
        self.assertEqual(32767+1000, reader.readUInt16())

        self.assertEqual(-128, reader.readInt8())
        self.assertEqual(255, reader.readUInt8())

    def test_writeDataDouble(self):
        writer = RemoteMeDataWriter()
        writer.writeDouble(-2147483648123123)
        writer.writeDouble(-12.345)
        writer.writeDouble(112.345)


        reader = RemoteMeDataReader(writer.getBytes())
        self.assertEqual(-2147483648123123, reader.readDouble())
        self.assertEqual(-12.345, reader.readDouble())
        self.assertEqual(112.345, reader.readDouble())



def getNow(self):
        return int(round(time.time() * 1000))


if __name__ == '__main__':
    unittest.main()