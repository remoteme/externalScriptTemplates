import socket
import threading

import struct


import logging



class RemoteMeDataWriter:

    def __init__(self):
        self.__logger = logging.getLogger('remoteMe.RemoteMeData')
        self.data=bytearray()


    def writeInt8(self,value):
        data=bytearray(struct.calcsize(">b"))
        struct.pack_into(">b",data,0,value)
        self.data.extend(data)

    def writeUInt8(self, value):
        data = bytearray(struct.calcsize(">b"))
        struct.pack_into(">B", data, 0, value)
        self.data.extend(data)



    def writeInt16(self, value):
        data = bytearray(struct.calcsize(">h"))
        struct.pack_into(">h", data, 0, value)
        self.data.extend(data)

    def writeUInt16(self, value):
        data = bytearray(struct.calcsize(">H"))
        struct.pack_into(">H", data, 0, value)
        self.data.extend(data)

    def writeString(self, value):
        data =  value.encode("utf-8")

        self.data.extend(data)
        self.writeInt8(0)

    def getBytes(self):
        return self.data


    def getBytesAsHexString(self):
        return  "".join("%02x " % b for b  in  self.data).upper()