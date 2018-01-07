import struct


def getUserMessage(userMessageSettings,receiverDeviceId,senderDeviceId,messageId,data):
    size = 7 + len(data)
    return struct.pack(">hhBhhh{0}s".format(len(data)), struct.MessageType.USER_MESSAGE._value_, size, userMessageSettings._value_, receiverDeviceId,
                       senderDeviceId, messageId, data)


def getWebRtcMessage(data):
    return struct.pack(">hh{0}s".format(len(data)),struct.MessageType.USER_MESSAGE._value_,len(data),data)


def getLogMessage(logLevel,message):
    byteArray = message.encode("utf-8")
    size = 1 + len(byteArray)+1
    return struct.pack(">hhB{0}sB".format(len(byteArray)),struct.MessageType.LOG._value_,size,logLevel._value_,byteArray,0)

def getRegisterLeafDeviceMessage(parentId,deviceId,deviceName,leafDeviceType):
    byteArray = deviceName.encode("utf-8")

    size = 4 + len(byteArray)+1+2
    return struct.pack(">hhhh{0}sBh".format(len(byteArray)),struct.MessageType.REGISTER_CHILD_DEVICE._value_,size,parentId,deviceId,byteArray,0,leafDeviceType)

def writeAddDataMessage(time,addDataMessageSetting,dataSeries):
    size = 8+1 + len(dataSeries)*10
    dataSeriesArray=[]

    for x in dataSeries:
        for b in struct.pack(">hd", x.seriesId, x.value):
            dataSeriesArray.append(b)

    dataSeriesArray=bytearray(dataSeriesArray)

    return 0
    #writeToPipe(struct.pack(">hhqB{0}s".format(len(dataSeriesArray)),struct.MessageType.ADD_DATA._value_,size,time,addDataMessageSetting._value_,dataSeriesArray))

